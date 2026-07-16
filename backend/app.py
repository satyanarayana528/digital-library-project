"""
Cloud-Based Digital Library System
-----------------------------------
Flask web app that:
  1. Uploads PDF books to Amazon S3
  2. Stores book metadata in Amazon DynamoDB
  3. Lists / searches books
  4. Generates a temporary download link (presigned URL) for each book

Requires AWS credentials to already be configured on the EC2 instance
(see Step 6.5 of the build guide: `aws configure`).
"""

import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, render_template, redirect, url_for, flash

# ---------------------------------------------------------------------------
# Configuration — edit these three values for your own AWS resources
# ---------------------------------------------------------------------------
AWS_REGION = "ap-south-1"
S3_BUCKET_NAME = "digital-library-books-yourname"   # must match the bucket you created
DYNAMODB_TABLE_NAME = "BooksMetadata"

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"  # needed for flash messages

# ---------------------------------------------------------------------------
# AWS clients (boto3 automatically uses the credentials set via `aws configure`)
# ---------------------------------------------------------------------------
s3_client = boto3.client("s3", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
books_table = dynamodb.Table(DYNAMODB_TABLE_NAME)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Home page — shows total book count and a few recent books."""
    try:
        response = books_table.scan()
        items = response.get("Items", [])
        items.sort(key=lambda x: x.get("upload_date", ""), reverse=True)
        recent_books = items[:5]
        total_books = len(items)
    except ClientError as e:
        flash(f"Could not load books: {e}")
        recent_books, total_books = [], 0

    return render_template("index.html", recent_books=recent_books, total_books=total_books)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload form (GET) and upload handler (POST)."""
    if request.method == "GET":
        return render_template("upload.html")

    # ---- POST: handle the actual upload ----
    file = request.files.get("book_file")
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()

    if not file or file.filename == "":
        flash("Please choose a PDF file to upload.")
        return redirect(url_for("upload"))

    if not allowed_file(file.filename):
        flash("Only PDF files are allowed.")
        return redirect(url_for("upload"))

    if not title or not author:
        flash("Title and Author are required.")
        return redirect(url_for("upload"))

    book_id = str(uuid.uuid4())
    safe_filename = file.filename.replace(" ", "_")
    s3_key = f"books/{book_id}_{safe_filename}"

    try:
        # 1. Upload the PDF to S3
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "application/pdf"},
        )

        # 2. Store metadata in DynamoDB
        books_table.put_item(
            Item={
                "book_id": book_id,
                "title": title,
                "author": author,
                "category": category if category else "Uncategorized",
                "upload_date": datetime.utcnow().isoformat(),
                "s3_key": s3_key,
            }
        )

        flash(f'"{title}" uploaded successfully!')
        return redirect(url_for("list_books"))

    except ClientError as e:
        flash(f"Upload failed: {e}")
        return redirect(url_for("upload"))


@app.route("/books")
def list_books():
    """List all books, optionally filtered by a search query (?q=...)."""
    query = request.args.get("q", "").strip().lower()

    try:
        response = books_table.scan()
        items = response.get("Items", [])
    except ClientError as e:
        flash(f"Could not load books: {e}")
        items = []

    if query:
        items = [
            b for b in items
            if query in b.get("title", "").lower()
            or query in b.get("author", "").lower()
            or query in b.get("category", "").lower()
        ]

    items.sort(key=lambda x: x.get("title", "").lower())
    return render_template("books.html", books=items, query=query)


@app.route("/download/<book_id>")
def download(book_id):
    """Generate a temporary presigned S3 URL and redirect the user to it.

    The bucket has Block Public Access ON, so direct S3 links won't work.
    A presigned URL grants time-limited access (default: 1 hour) without
    making the bucket itself public.
    """
    try:
        response = books_table.get_item(Key={"book_id": book_id})
        item = response.get("Item")
        if not item:
            flash("Book not found.")
            return redirect(url_for("list_books"))

        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": item["s3_key"]},
            ExpiresIn=3600,  # 1 hour
        )
        return redirect(url)

    except ClientError as e:
        flash(f"Could not generate download link: {e}")
        return redirect(url_for("list_books"))


@app.route("/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    """Optional: delete a book from both S3 and DynamoDB."""
    try:
        response = books_table.get_item(Key={"book_id": book_id})
        item = response.get("Item")
        if item:
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=item["s3_key"])
            books_table.delete_item(Key={"book_id": book_id})
            flash(f'"{item["title"]}" deleted.')
        else:
            flash("Book not found.")
    except ClientError as e:
        flash(f"Delete failed: {e}")

    return redirect(url_for("list_books"))


if __name__ == "__main__":
    # For local testing only. On EC2, prefer running via gunicorn:
    #   gunicorn -w 2 -b 0.0.0.0:80 app:app
    app.run(host="0.0.0.0", port=80, debug=True)
