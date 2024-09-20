# Data Science Portfolio Repository

This repository contains a set of data science projects showcased through a Streamlit application. Each project highlights different aspects of machine learning, computer vision, and data analytics. The main aim of the repository is to demonstrate practical applications of data science techniques, ranging from object recognition models to visualizing sports analytics.

## Projects

### 1. **Object Recognition Model using MobileNet SSD**
The first project is an object recognition system built using the MobileNet Single Shot Detector (SSD) model. MobileNet SSD is a lightweight and efficient neural network model for detecting objects in images.
  
Users can upload an image through the Streamlit interface, and the model will identify and label objects within the media. The focus is on efficient deployment for real-world applications, making use of lightweight architecture to handle real-time processing tasks.

### 2. **Tennis Head-to-Head Analytics Dashboard**
The second project is a data analytics tool that visualizes head-to-head statistics of tennis matches between two players. This interactive dashboard enables users to:

- Compare historical match data between two players.
- Visualize win/loss records, match outcomes by surface type, and other relevant statistics.
- Gain insights into player performance trends and strategic advantages.

The app provides users with an easy-to-use interface to explore historical tennis data and analyze key metrics. It’s built to be dynamic, allowing users to select any two players and filter the data accordingly.

## Dependencies

This project uses **Poetry** for dependency management, ensuring a clean and isolated environment for package installation. All required libraries and their versions are specified in the `pyproject.toml` file.

To install dependencies using Poetry, first ensure that Poetry is installed on your machine. Then, run:

```bash
poetry install
```

This will create a virtual environment and install all necessary packages for the application to run.
  
## Running the Streamlit App Using Docker

The Streamlit application is containerized with Docker for easy deployment across different environments. Follow the steps below to build and run the application using Docker.

1. **Clone the repository:**

   First, clone the repository to your local machine using the following command:
   ```bash
   https://github.com/Trung-Dan-Phan/streamlit-portfolio.git
   ```

2. Navigate to the project directory:

   Change into the project directory where the Dockerfile is located:
   ```bash
   cd your-repository
   ```

   Replace `your-repository` with the name of your project directory.


3. **Build the Docker image:**

   Open the terminal, and in the root directory of the repository, run the following command to build the Docker image:

   ```bash
   docker build -t streamlit-app .
   ```

4. **Run the Docker container:**

   Once the image is built, you can run the container with:

   ```bash
   docker run -p 8501:8501 streamlit-app
   ```

   This will start the Streamlit application, which will be accessible at `http://localhost:8501` in your browser.

## How to Use the Application

Once the Streamlit app is running, you can interact with the projects as follows:
- **Object Recognition**: Upload an image file (you can take jpg files in the `images` folder for inspiration), and the model will process it to identify objects within the media.
- **Tennis Analytics**: Input the names of two tennis players, and the dashboard will display head-to-head statistics, match history, and more.