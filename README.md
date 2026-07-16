### 📚 Cloud-Based Digital Library System
 
## 📖 About the Project

The **Cloud-Based Digital Library System** is a web application developed using **Flask** and **Amazon Web Services (AWS)** to provide secure storage, management, and access to digital books. The system enables users to upload, browse, search, download, and manage PDF books through a simple web interface.

The project demonstrates cloud deployment using AWS services such as **Amazon EC2, Amazon VPC, Amazon S3, Amazon DynamoDB, and Amazon CloudWatch**. It provides a scalable and reliable solution for digital library management while reducing the dependency on traditional library systems.


## 🎯 Project Objectives

 ✅ Develop a cloud-based digital library application
 ✅ Provide secure storage for PDF books
 ✅ Enable users to upload, browse, search, and download books
 ✅ Store book metadata using Amazon DynamoDB
 ✅ Deploy the application on Amazon EC2
 ✅ Monitor the application using Amazon CloudWatch

## ✨ Key Features

## 📚 Book Management

* Upload PDF Books
* Browse Available Books
* Search Books
* Download Books
* Delete Books


## ☁️ Cloud Features

* Amazon EC2 Hosting
* Amazon S3 File Storage
* Amazon DynamoDB Database
* Amazon VPC Networking
* Security Groups
* Amazon CloudWatch Monitoring



## 🔍 Search Features

* Search by Title
* Search by Author
* Search by Category
* Fast Metadata Retrieval


## 🏗 Project Directory Structure

```text
Cloud-Based-Digital-Library-System
│
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── books.html
│
├── static/
│   ├── css/
│   ├── js/
│
├── uploads/
│
├── config.py
│
└── README.md
```



## ⚙️ Installation Guide

## Step 1 — Launch Amazon EC2

Create an Ubuntu EC2 instance.



## Step 2 — Install Required Software

```bash
sudo apt update
sudo apt install python3 python3-pip git
pip3 install flask boto3
```



## Step 3 — Clone Repository

```bash
git clone <repository-url>
```

---

## Step 4 — Configure AWS

Configure AWS credentials.

```bash
aws configure
```

---

## Step 5 — Create AWS Resources

* Amazon VPC
* EC2 Instance
* Security Groups
* Amazon S3 Bucket
* DynamoDB Table
* CloudWatch Monitoring

---

## Step 6 — Run the Application

```bash
python3 app.py
```

Access the application using the EC2 Public IP.

---

# 🚀 Application Workflow

```text
User
   │
   ▼
Flask Web Application
   │
   ▼
Amazon EC2
   │
   ├────────► Amazon S3
   │          (Stores PDF Books)
   │
   ├────────► Amazon DynamoDB
   │          (Stores Book Metadata)
   │
   ▼
Amazon CloudWatch
(Monitoring)
```

---

# ☁️ AWS Services Used

* 🌐 Amazon VPC
* 🖥 Amazon EC2
* 🔐 Security Groups
* 📚 Amazon S3
* 🗄 Amazon DynamoDB
* 📊 Amazon CloudWatch

---

# 💻 Technology Stack

### Backend

* Python
* Flask
* Boto3

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Cloud Platform

* Amazon Web Services (AWS)

---

# 👥 Team Responsibilities

## ☁️ AWS Cloud Infrastructure

* Amazon VPC
* Amazon EC2
* Security Groups
* Amazon S3
* Amazon DynamoDB
* Amazon CloudWatch

⬇️

## 💻 Backend Development

* Flask Application
* AWS Integration
* File Upload
* Search Functionality
* Download Functionality

⬇️

## 🎨 Frontend Development

* HTML
* CSS
* Bootstrap
* Responsive User Interface

⬇️

## 📄 Documentation

* Project Report
* Presentation (PPT)
* GitHub Repository

---

# 🌟 Project Output

✔ Cloud-Based Deployment

✔ Secure PDF Storage

✔ Fast Book Search

✔ Digital Library Management

✔ Scalable AWS Infrastructure

✔ Responsive Web Application

✔ Cloud Monitoring

---

# 🚀 Future Enhancements

* User Authentication
* Role-Based Access Control
* Book Recommendation System
* Mobile Application
* Email Notifications
* REST API Integration

---



