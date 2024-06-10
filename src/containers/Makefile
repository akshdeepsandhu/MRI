DOCKERHUB_USERNAME=trantor2295
IMAGE_VERSION=1.1

# CPU Image
CPU_IMAGE_NAME=imoco_cpu
CPU_DOCKERFILE=Dockerfile.imoco-cpu
CPU_CONTAINER_NAME=imoco_cpu_container

# GPU Image
GPU_IMAGE_NAME=imoco_gpu
GPU_DOCKERFILE=Dockerfile.imoco-gpu
GPU_CONTAINER_NAME=imoco_gpu_container

.PHONY: help build_cpu build_gpu run_cpu run_gpu stop_cpu stop_gpu clean_cpu clean_gpu push_cpu push_gpu

help:
	@echo "Available targets:"
	@echo "  make build_cpu  - Build the CPU Docker image"
	@echo "  make build_gpu  - Build the GPU Docker image"
	@echo "  make run_cpu    - Run the CPU Docker container"
	@echo "  make run_gpu    - Run the GPU Docker container"
	@echo "  make stop_cpu   - Stop the CPU Docker container"
	@echo "  make stop_gpu   - Stop the GPU Docker container"
	@echo "  make clean_cpu  - Stop and remove the CPU Docker container"
	@echo "  make clean_gpu  - Stop and remove the GPU Docker container"
	@echo "  make push_cpu   - Push the CPU image to Docker Hub"
	@echo "  make push_gpu   - Push the GPU image to Docker Hub"

build_cpu:
	docker build -t $(DOCKERHUB_USERNAME)/$(CPU_IMAGE_NAME):$(IMAGE_VERSION) -f $(CPU_DOCKERFILE) .

build_gpu:
	docker build -t $(DOCKERHUB_USERNAME)/$(GPU_IMAGE_NAME):$(IMAGE_VERSION) -f $(GPU_DOCKERFILE) .

run_cpu:
	docker run --name $(CPU_CONTAINER_NAME) $(DOCKERHUB_USERNAME)/$(CPU_IMAGE_NAME):$(IMAGE_VERSION)

run_gpu:
	docker run --gpus all --name $(GPU_CONTAINER_NAME) $(DOCKERHUB_USERNAME)/$(GPU_IMAGE_NAME):$(IMAGE_VERSION)

stop_cpu:
	docker stop $(CPU_CONTAINER_NAME)

stop_gpu:
	docker stop $(GPU_CONTAINER_NAME)

clean_cpu:
	docker stop $(CPU_CONTAINER_NAME)
	docker rm $(CPU_CONTAINER_NAME)

clean_gpu:
	docker stop $(GPU_CONTAINER_NAME)
	docker rm $(GPU_CONTAINER_NAME)

push_cpu:
	docker push $(DOCKERHUB_USERNAME)/$(CPU_IMAGE_NAME):$(IMAGE_VERSION)

push_gpu:
	docker push $(DOCKERHUB_USERNAME)/$(GPU_IMAGE_NAME):$(IMAGE_VERSION)
