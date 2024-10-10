# Energy Community Simulator

## Description

The Energy Community Simulator is a tool designed to model and simulate the behavior of an energy community composed of multiple participants or profiles. These profiles represent different types of households, each with unique energy consumption and production characteristics. Household profiles can be created by importing real data from a file or by simulating them through the configuration of various assets, such as solar panels, lighting, electric kitchens, dishwashers, and more.

The simulator allows users to configure a range of parameters, including community renewable energy generation (e.g., solar, wind), storage capacities (not implemented yet for community), energy sharing rules, and energy pricing plans. It provides insights into how the community interacts, how energy is exchanged between participants, and the overall efficiency of energy usage within the community.

The simulator can be used for:

- Analyzing self-consumption rates
- Simulating peak demand scenarios
- Modeling economic benefits of energy sharing
- Evaluating the impact of different policies on energy distribution
- By adjusting the configuration of each profile, users can gain a deeper understanding of how various factors influence the performance and sustainability of an energy community.
- Optimizing the shares of each household

## Getting Started

Follow these instructions to get your project up and running on your local machine.

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/LiamViader/EnergyCommunitiesSimulator
    cd EnergyCommunitiesSimulator
    ```

2. **Create and activate a virtual environment:**
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```


### Reading the docs

docs are ubicated at /docs/build/html/index.html

### ReGenerating docs

use 
```bash
    cd docs
    .\make.bat html
```


### Running the Project
<!-- TODO -->
```bash
python main.py
```
### Usage
<!-- TODO: Add usage instructions later (could implement the input using a yaml and optional parameters for files. Or just implement the visual interactive interface)--> 
### Contributing
<!-- TODO -->
### License
<!-- TODO -->
### Acknowledgments

<!-- TODO -->
