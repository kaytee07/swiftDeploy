# SwiftDeploy
SwiftDeploy is a one-click deployment tool designed to simplify the process of managing Docker containers and clusters. With SwiftDeploy, you can easily deploy clusters of servers and interact with containers without requiring in-depth knowledge of Docker. This project was created with the aim of providing a valuable resource for developers within the community.

## Usage
To get started with SwiftDeploy, you can run the following command:
```
python3 -m api.v1.app
```

## Features
### User Registration and Login
SwiftDeploy offers a secure and personalized user experience through user registration and login functionality. This feature enhances the security of the platform and allows users to access personalized services.

### Container Pulling
With SwiftDeploy, users can effortlessly access a vast library of container images from Docker Hub and other repositories. This feature expands software possibilities and simplifies the process of acquiring containerized applications.

### Container Deployment
SwiftDeploy enables users to start containers on demand, streamlining the process of running applications within isolated environments. This promotes efficiency and optimal resource utilization.

## Configuration Options
```
SD_MYSQL_USER='user'               # MySQL database user
SD_MYSQL_PWD='password'            # MySQL database password
SD_MYSQL_HOST='localhost'          # MySQL database host
SD_MYSQL_DB='docker_db'            # MySQL database name
SD_TYPE_STORAGE='db'               # Storage type (e.g., 'db' or 'file')
SD_API_HOST='0.0.0.0'              # API host (0.0.0.0 for all network interfaces)
SD_API_PORT=5001                   # API port
SD_SESSION_KEY='mkhailo'           # Session encryption key
```

## Setting Environment Variables
To set the environment variables, follow these steps on a Unix-based system (Linux or macOS):

1. Create a .env file in your project's root directory:
```
touch .env
```

2. Open the .env file in a text editor and add the environment variables with their values as shown above.

3. Save the file.

4. Before running your project, load the environment variables from the .env file using a tool like python-dotenv or by running:

```
source .env
```

If you're using a different platform or development environment, consult its documentation for guidance on setting environment variables.

SwiftDeploy simplifies the process of deploying and managing containers, making it accessible to developers withoutextensive Docker expertise. Use the provided instructions to configure the project and get started quickly. Enjoy streamlined container management with SwiftDeploy!