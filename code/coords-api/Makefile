REGISTRY=ghcr.io
NAMESPACE=shrimpsizemoose
APP=evaporating-image-coords-api
VERSION=0.1.0
PORT=9099

SERVICE_TAG=${REGISTRY}/${NAMESPACE}/${APP}:${VERSION}


@build: *.go Dockerfile
	docker build --tag ${SERVICE_TAG} .


@push:
	docker push ${SERVICE_TAG}
