# Workout Progress Dashboard

This Workout Dashboard is an interactive tool designed to help us users track and optimize our fitness routines. It integrates workout data and analytics into an easy-to-use interface allowing us to monitor our progress, plan workouts effectively, and achieve our fitness goals.

Features:
- Workout Tracking: Log and view your exercises, sets, reps, and weights.
- Analytics: Visualize trends in your performance over time with graphs and insights.
    
    KPI's
    - Current week within the program starts on a Monday and ends on a Sunday.
    - Current month includes all workout records within the current month.
    - Total records includes all record within dataset.

## Getting Started

### Prerequisites

- Python 3.11
- pip

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Install the required dependencies:

    ```bash
    pip install streamlit pandas matplotlib
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

4. Open the provided URL in your web browser to view the dashboard.

## Usage
app.py
- Use the sidebar to select a muscle group.
- View an overview of workout data for the selected muscle group.
- Explore weight progression over time for each exercise in the selected muscle group.

## File Structure

- `app.py`: The main Python script for the Streamlit app.
- `path/to/your/csv/file.csv`: Replace with the actual path to your workout data CSV file.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and suggestions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://www.streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

## Author

Alex Guerrero
