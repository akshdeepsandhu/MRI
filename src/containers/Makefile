DOCKERHUB_USERNAME=trantor2295
IMAGE_VERSION=1.0
IMAGE_NAME=imoco_cpu
DOCKERFILE=Dockerfile.imoco-cpu
CONTAINER_NAME=imoco_cpu_container

.PHONY: help build run stop clean push

help:
	@echo "Available targets:"
	@echo "  make build      - Build the Docker image"
	@echo "  make run        - Run the Docker container"
	@echo "  make stop       - Stop the Docker container"
	@echo "  make clean      - Stop and remove the Docker container"
	@echo "  make push       - Push the image to Docker Hub"

build:
	docker build -t $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMAGE_VERSION) -f $(DOCKERFILE) .

run:
	docker run --name $(CONTAINER_NAME) $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMAGE_VERSION)

stop:
	docker stop $(CONTAINER_NAME)

clean:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

push:
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMAGE_VERSION)
