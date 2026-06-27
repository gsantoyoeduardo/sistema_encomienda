FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o shipping_service_go main.go

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/shipping_service_go .

EXPOSE 8081

CMD ["./shipping_service_go"]
