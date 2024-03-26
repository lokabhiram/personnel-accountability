# Personnel Accountability System

## Overview
The Personnel Accountability System is a computer vision-based application that tracks and monitors the movement of people within a specified area. It counts the number of individuals entering and exiting the area, providing real-time updates through a web interface.

## Features
- **Visitor Counting**: Accurately counts the number of people entering and exiting a designated zone.
- **Real-time Updates**: Provides real-time updates on the number of people currently inside the area.
- **Web Interface**: Accessible web interface for easy monitoring of visitor count.
- **Computer Vision**: Utilizes computer vision techniques for person detection and tracking.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/lokabhiram/personnel-accountability.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python main.py
    ```
4. Access the web interface at `http://localhost:5000/visitor_count` to view the visitor count.

## Usage
- Ensure that the video file (`test_1.mp4`) is located in the appropriate directory or provide the correct path to the video file.
- Adjust parameters such as line positions, area thresholds, and kernel sizes as per your specific requirements.
- Customize the application according to your use case.

## Contributors
- [Lokabhiram](https://github.com/lokabhiram) - Main Developer

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

