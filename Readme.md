run locally with docker:

docker build -t my-flask-app2 . && docker run -p 8000:5000 my-flask-app2

docker tag fastapi-app us-central1-docker.pkg.dev/investmentbot-425621/docker-repo/api:1.0

docker push us-central1-docker.pkg.dev/investmentbot-425621/docker-repo/api:1.0