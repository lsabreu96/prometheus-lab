# Mini mini lab Prometheus
Baseado nesse artigo da [RedHat](https://developers.redhat.com/articles/2023/11/30/how-set-and-experiment-prometheus-remote-write) que tem esse [repo](https://github.com/yftacherzog/prom-remote-write).

A ideia é testar o protocolo remote-write do Prometheus e validar o comportamento de que as métrica são escritas em ambas instâncias e não apenas em uma

## App
O app é uma aplicação Flask bem simples que usa o uWSGI na frente para poder se comunicar via nginx. A aplicação processa o caminho que as métricas são escritas e expõe via endpoint
