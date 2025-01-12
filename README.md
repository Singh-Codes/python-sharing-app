# Python File Sharing App 🚀

A secure and user-friendly file sharing application built with Python that works over Wide Area Network (WAN). Share files easily with anyone across the internet using secure access keys and ngrok tunneling.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

- 📤 Easy file upload and sharing
- 🔐 Secure access with unique keys
- 🌐 Works over WAN using ngrok tunneling
- 🖥️ Simple web interface
- 📱 Command-line interface (CLI)
- 💾 Local file storage with metadata
- ⚙️ Configurable settings
- 🔄 Cross-platform support

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- A free ngrok account ([Sign up here](https://ngrok.com/))
- Git (optional, for cloning)

## 🔧 Installation Guide

### Windows

1. Install Python:
   - Download from [python.org](https://python.org)
   - Run installer (✅ Check "Add Python to PATH")
   - Verify in CMD: `python --version`

2. Clone repository:
   ```bash
   git clone https://github.com/Singh-Codes/python-sharing-app.git
   cd python-sharing-app
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### macOS

1. Install Python using Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python
   ```

2. Clone repository:
   ```bash
   git clone https://github.com/Singh-Codes/python-sharing-app.git
   cd python-sharing-app
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Linux (Ubuntu/Debian)

1. Install requirements:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

2. Clone repository:
   ```bash
   git clone https://github.com/Singh-Codes/python-sharing-app.git
   cd python-sharing-app
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## ⚙️ Configuration

1. Get your ngrok authtoken:
   - Sign up at [ngrok.com](https://ngrok.com)
   - Go to [your dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
   - Copy your authtoken

2. Set up configuration:
   ```bash
   cp config.template.ini config.ini
   ```
   Edit `config.ini`:
   ```ini
   [ngrok]
   auth_token = your_ngrok_authtoken_here

   [server]
   max_file_size = 16
   port = 5000
   ```

## 🚀 Usage

### Starting the Server

1. Navigate to the project directory
2. Run the server:
   ```bash
   python server.py
   ```
   You'll see the public URL when the server starts.

### Using the Client

1. Open a new terminal
2. Run the client:
   ```bash
   python client.py
   ```

### Sharing Files

1. Select "Upload File" in the client
2. Enter file path when prompted
3. You'll receive:
   - Public access link
   - Access key
4. Share both with your recipient

### Accessing Shared Files

Recipients can:
1. Open the shared link in any browser
2. Enter the access key
3. Download the file

## 🔒 Security Features

- Secure file access with unique keys
- HTTPS encryption via ngrok
- Access logging
- File size limits
- Input validation

## 🛠️ Troubleshooting

### Ngrok Issues
- Verify authtoken in config.ini
- Check internet connection
- Ensure no other ngrok tunnels are running

### Upload Problems
- Check file permissions
- Verify file size limit
- Ensure server is running

### Connection Issues
- Check server status
- Verify URL
- Check firewall settings

## 📝 Contributing

1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit changes:
   ```bash
   git commit -m 'Add YourFeature'
   ```
4. Push to branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Support

- Star this repository
- Report issues
- Submit pull requests
- Share with others

## 🙏 Acknowledgments

- Flask team for the web framework
- Ngrok team for tunneling service
- Python community for inspiration

---
Made with ❤️ by [Singh-Codes](https://github.com/Singh-Codes)
