# 📌 Event Detection System Using Computer Vision

## 🔍 Project Overview  
This project aims to develop an event detection system using Computer Vision techniques to identify critical events and objects in real-world scenarios. The system integrates multiple deep learning models, including YOLO, RT-DETR, and DINO, and provides real-time notifications via LINE.  

---  

## 🎯 Objectives  

- **📚 Study and Develop Computer Vision Techniques:**  
  - Implement object and event detection using YOLO, RT-DETR, and DINO models.  

- **🛠️ System Development:**  
  - Build a robust Computer Vision system applicable to real-world situations, enhancing safety and security.  

- **🚑 Key Features:**  
  - Fall detection for humans  
  - Infant regurgitation detection  
  - Venomous animal detection  
  
- **🛡️ Safety Enhancement:**  
  - Supports personnel in managing hazardous situations through real-time monitoring and notifications.  

---  

## 🏗️ Technologies Used  

- **Programming Language:** Python  
- **Deep Learning Frameworks:** PyTorch, TensorFlow  
- **Models Used:** YOLO, RT-DETR, DINO, CNN  
- **Hardware:** Raspberry Pi 5, CCTV cameras, webcams  
- **Notification System:** LINE API  

---  


## 🚀 Installation  

### 1️⃣ Clone the Repository  
```bash  
git clone https://github.com/Kyaputan/my-senior-project.git  
cd my-senior-project  
```  

### 2️⃣ Configure API Keys  
Before running the setup, update your `.env` file with the necessary API keys for the system to function correctly.  

### 3️⃣ Run the Setup  
- **For Raspberry Pi**  
  ```bash
  sudo apt update  
  sudo apt install ntp  
  sudo timedatectl set-ntp true  
  sudo apt install cmake
  python setup-pi.py  
  ```    
- **For Windows**  
  ```bash  
  python setup-Window.py  
  ```    

### 4️⃣ Run the System  
- **With GUI**  
  ```bash  
  python main-ui.py  
  ```    
- **Without GUI**  
  ```bash  
  python main-uiless.py  
  ```


---  

## 📧 Contact Information  

- **👤 Developer:** Ratchata Singkhet  
- **📩 Email:**  
  - 64200350@kmitl.ac.th  
  - singkhet1@gmail.com  
- **🏫 Institution:** King Mongkut’s Institute of Technology Ladkrabang  
  - Chumphon Khet Udomsak Campus  
