# DataToolbox

![FeaturedTools](/docs/images/featured_tools.PNG)

Data Toolbox provides a collection of diverse tools for various tasks including
data manipulation, translation, mapping, and more. It is a
web based project developed in Python and uses the Streamlit package to provide
the user interface.

[Toolbox tools overview and descriptions](DataToolbox Tools) -- Description of what each tool does

[Home](Home) -- Main Wiki with good-to-know information

## Getting Started

The Data Toolbox team assumes the development environment and target deployment
operating system is Windows. Users of other operating systems have provided
feedback that helped them create a working development environment which is
shared here in the hope it is helpful. If you run into any more issues we
welcome feedback to improve. Before diving deeper into development begin with
the following setup steps depending on your environment.

### Docker

A detaled description on how our project uses Dockers is depicted in the wiki below.  
However at a base level there is a Dockerfile-base that has all the system configurations
and a Dockerfile that has all the code changes.  The Dockerfile-base is downloaded from the
wildfires Container Registry similarly to how it's done with Docker Hub.

Follow these steps to build a Docker image

1. set up your account up with a [Personal Access Token](https://gitlab.wildfireworkspace.com/-/user_settings/personal_access_tokens)
1. log into Docker via the terminal<br>
```bash
docker login registry.wildfireworkspace.com/eop/streamlit-1.0 -u YOUR_USERNAME_HERE
```
1. then build dockers as normal<br>

Docker will pull base images as needed from the wildfire Container Registry
 
[Wildfire Docker wiki](https://gitlab.wildfireworkspace.com/eop/streamlit-1.0/-/wikis/Docker-Base-Image)

### Windows

Install the following two dependencies:

1. [C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
1. [Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)

### Linux

```bash
sudo apt install python3.11-dev gcc ffmpeg libkrb5-dev
```

### Mac

```bash
brew install libomp
```

## Getting Started (Python)

Data Toolbox is developed with Python 3.11 for compatibility with dependencies.
Ensure you have the appropriate version installed and accessible.
To run the Data Toolbox (using python locally) follow the steps below:

1. Clone this repository to your local environment.

    ```cmd
    git clone https://gitlab.wildfireworkspace.com/eop/streamlit-1.0.git
    ```
   
### Linux / MacOS
1. From the root directory run the initialization shell script:

```cmd
# Make the script executable
chmod +x dev-init-unix.sh

# Run the script 
sh dev-init-unix.sh
```
### Windows
1. Set up virtual environment (optional but highly recommended)

    From within the directory you just cloned set up a virtual Python
    environment using a tool like `venv` or `anaconda.`

    ```cmd
    # Create the virtual environment ensuring to specify the correct version
    py -3.11 -m venv venv

    # Activation
    .\venv\Scripts\activate.bat
    ```

1. After activating the virtual environment install the required dependencies.
    You can install them using the following command:

    ```cmd
    cd src
    py -m pip install -r requirements.txt
    ```

1. Export required Environment Variables
    You can set SL_ANALYTICS_PATH to any empty directory. Analytics logs
    will be written to it.

    ```bash
    SET SL_ANALYTICS_PATH=./analytics/
    ```

    If you need to disable the analytics, you can use this Environment Variable.

    ```bash
    SET LOG_ANALYTICS=False
    ```

1. Start the Data Toolbox - From `src/` run the following command:

    ```cmd
    streamlit run main.py
    ```

## Getting Started (Docker)

To run the Data Toolbox using Docker run the command below:

```cmd
docker compose --env-file ./environment/common.env up --build
```

To run an individual tool within the Data Toolbox using Docker run the command below:

```cmd
docker compose --env-file ./environment/common.env up --build <toolname>
```

Because we have several different docker files, to specify which docker-compose.yml you'd like to use, run this command below:

```cmd
docker compose -f <docker-compose-of-your-choice.yml> --env-file ./environment/common.env up --build
```

docker-compose.yml - This yml file is for production and not meant for running on a dev machine/personal computer due to the Nvidia resources section

docker-compose-cpu.yml - This yml file can be used outside of production, and run on a regular computer

docker-compose-autoupdate.yml - This yml file is meant for dev and dev only. When you run the containers using this file, your code will live reload as you work in your IDE with the files on your computer. The files will bind mount from your dev computer to the container. There are some limitations - certain files will require a docker rebuild such as main.py files, configs, requirements.txt, etc. This is only meant to cover the files that contain the majority of the app logic that a developer would traditionally be working on. If you want to see which files are included, look at the "volumes" section within the docker-compose-autoupdate.yml for the particular tool you are working on. These files are included in the live reloading.

## Caching Models

To cache all models locally, you can run the bash script in the root of the application.
This will download all models and store them in a directory of your choice. Set the
directory using the HF_HOME environment variable. If this variable is not set, the
script will prompt you for it.

```bash
chmod +x cache_all_models.sh
source cache_all_models.sh
```

HF_HOME must be set to an ABSOLUTE path to a directory. It will not understand shortcuts.
Running the script using the above method will preserve the HF_HOME environment variable
set during script execution in your shell.

To run without saving the environment variable use the following:

```bash
chmod +x cache_all_models.sh
./cache_all_models.sh
```

## Admin Tools

Add the query parameter `admin` to the URL path to enable hidden admin views.

## Contributing

Please reach out if you're interested in helping out or have an interesting idea
you think we can help with. Review [CONTRIBUTING.md](docs/CONTRIBUTING.md)
for more information.
