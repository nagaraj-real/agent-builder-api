docker build -t nagaraj23/agent-builder-api:latest . | tee deploy.txt
docker tag nagaraj23/agent-builder-api:latest ghcr.io/nagaraj-real/agent-builder-api:latest
docker pull mongo:latest | tee install_output.txt
docker tag mongo ghcr.io/nagaraj-real/agent-builder-mongo:latest

docker push ghcr.io/nagaraj-real/agent-builder-api:latest | tee install_output.txt
docker push ghcr.io/nagaraj-real/agent-builder-mongo:latest | tee install_output.txt

docker system prune -a -f
