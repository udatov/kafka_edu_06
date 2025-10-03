# Kafka Edu Module 6

## Информация:
- Начал выполнять задание в Yandex Cloud, но за 4 дня закончились деньги и личные и по предоставленному промокоду. 
- Задание выполнено через DockerCompose!

## Технические инструкции

### Назначение каждого компонента и их взаимосвязи.
services:
  x-kafka-common:
  kafka-0:
  kafka-1:
  kafka-2:
  schema-registry:
  nifi:

## Задание 1.Развёртывание и настройка Kafka-кластера
### Шаг 1. Запуск решения через Docker Compose.
```bash 
docker compose up -d
```

### Шаг 2. Создайте топик с 3 партициями и коэффициентом репликации 3:
```bash
docker compose exec kafka-0 kafka-topics.sh --create --topic module_6 --partitions 3 --replication-factor 3 --bootstrap-server kafka-0:9092     --config cleanup.policy=delete --config retention.ms=86400000 --config segment.bytes=1073741824
```
** cleanup.policy=delete — обычный режим удаления старых данных
** retention.ms=86400000 — 1 день хранения
** segment.bytes=1073741824 — 1 ГБ сегменты


### Шаг 3. Настройте Schema Registry
JSON-схема [user-value.avsc]:
```json
{"schema":
  "{
    "type": "record",
    "name": "User",
    "fields": [
      {"name": "id", "type": "int"},
      {"name": "username", "type": "string"},
      {"name": "registered", "type": "boolean"}
    ]
  }"
}
```
* Регистрация схемы через curl:
```bash
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"User\",\"namespace\":\"ru.practicum\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"},{\"name\":\"username\",\"type\":\"string\"},{\"name\":\"registered\", \"type\": \"boolean\"}]}"}' http://localhost:8081/subjects/user-value/versions
```
```powershell
Invoke-WebRequest -Uri http://localhost:8081/subjects/user-value/versions -Method POST -Headers @{"Content-Type"="application/vnd.schemaregistry.v1+json"} -Body '{"schema": "{\"type\":\"record\",\"name\":\"User\",\"namespace\":\"ru.practicum\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"},{\"name\":\"username\",\"type\":\"string\"},{\"name\":\"registered\", \"type\": \"boolean\"}]}"}'
```

### Шаг 4. Проверьте работу Kafka:
* Получение списка схем:
```bash
curl http://localhost:8081/subjects
```
StatusCode        : 200
StatusDescription : OK
Content           : {91, 34, 117, 115...}
RawContent        : HTTP/1.1 200 OK
                    X-Request-ID: 68d5bd75-1f40-4b29-a395-0ff2b91b952e
                    Vary: Accept-Encoding, User-Agent
                    Content-Length: 14
                    Content-Type: application/vnd.schemaregistry.v1+json
                    Date: Thu, 02 Oct 2025...
Headers           : {[X-Request-ID, 68d5bd75-1f40-4b29-a395-0ff2b91b952e], [Vary, Accept-Encoding, User-Agent], [Content-Length, 14], [Content-Type,
                    application/vnd.schemaregistry.v1+json]...}
RawContentLength  : 14

* Получение версий схемы:
```bash
curl http://localhost:8081/subjects/user-value/versions
```
StatusCode        : 200
StatusDescription : OK
Content           : {91, 49, 93}
RawContent        : HTTP/1.1 200 OK
                    X-Request-ID: d13e3425-5384-484f-b535-cc8b362e2b2c
                    Vary: Accept-Encoding, User-Agent
                    Content-Length: 3
                    Content-Type: application/vnd.schemaregistry.v1+json
                    Date: Thu, 02 Oct 2025 ...
Headers           : {[X-Request-ID, d13e3425-5384-484f-b535-cc8b362e2b2c], [Vary, Accept-Encoding, User-Agent], [Content-Length, 3], [Content-Type,
                    application/vnd.schemaregistry.v1+json]...}
RawContentLength  : 3

* Описание топика:
```bash
docker compose exec kafka-0 kafka-topics.sh --describe --topic module_6 --bootstrap-server kafka-0:9092
```
Topic: module_6 TopicId: 7WmlM8R8Tw2dkZRZvmcptA PartitionCount: 3       ReplicationFactor: 3    Configs: cleanup.policy=delete,segment.bytes=1073741824,retention.ms=86400000
        Topic: module_6 Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
        Topic: module_6 Partition: 1    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: module_6 Partition: 2    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2


### Проверка с помошью python producer/consumer
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r clients/requirements.txt
python clients/producer.py
# Message delivered to module_6 [1]
python clients/consumer.py
# Received message: {"id": "1", "username": "Ivan", "registered": true}
```

## Задание 2. Интеграция Kafka с внешними системами (Apache NiFi)
### NIFI:
http://localhost:8080/nifi/

Поток данных NIFI: 
GenerateFlowFile -- PublishKafka (топик module_06_out) -- ConsumeKafka (топик module_06_out)
Nifi принтскрины подтверждения в папке [nifi](nifi)
* Создан процессор GenerateFlowFile
* Создан процессор PublishKafka (топик module_06_out)
* Настроена связь GenerateFlowFile -- PublishKafka
* Создан процессор ConsumeKafka (топик module_06_out)
* После процессоров установлены очереди подсчета успешных потоков!

### Остановка сервисов 
```bash 
docker compose down                                
```
