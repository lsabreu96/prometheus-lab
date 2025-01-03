import re
from typing import Tuple

class uWSGILogParser:

    def __init__(self, log_file_path:str, log_position:int=0):
        self.log_file_path = log_file_path
        self.log_position = log_position

    def parse_uwsgi_logs(self) -> Tuple[str, int]:
        """
        Faz parse dos logs do uWSGI e retorna as métricas no formato `text/plain` 
        para serem usadas pelo Prometheus.

        Args:
        log_file_path (str): O caminho para o arquivo de log do uWSGI.
        log_position (int): A posição para começar a ler o arquivo de log.

        Returns:
        Tuple[str, int]: Uma tupla contendo as métricas no formato `text/plain` e a nova posição para começar a ler o arquivo de log.
        """
        
        log_pattern = re.compile(
            r'.*\[(?P<timestamp>.+?)\] (?P<method>\w+) (?P<path>\S+) => '
            r'generated (?P<size>\d+) bytes in (?P<time>[\d.]+) (?P<unit>msecs|secs) '
            r'\(HTTP/(?P<http_version>\d\.\d) (?P<status>\d+)\).*'
        )

        metrics = {}

        # Abrir o arquivo de log no modo leitura
        with open(self.log_file_path, "r") as log_file:
            # Mover para a última posição lida
            log_file.seek(self.log_position)
            for line in log_file:
                match = log_pattern.match(line)
                if match:
                    path = match.group("path")
                    status = match.group("status")
                    size = int(match.group("size"))
                    time = float(match.group("time"))
                    unit = match.group("unit")

                    # Converter tempo para milissegundos se necessário
                    if unit == "secs":
                        time *= 1000

                    # Chave única para combinar dimensões
                    key = (path, status)

                    if key not in metrics:
                        metrics[key] = {"total_requests": 0, "total_size": 0, "total_time": 0}

                    metrics[key]["total_requests"] += 1
                    metrics[key]["total_size"] += size
                    metrics[key]["total_time"] += time

            # Atualizar a posição para o fim do arquivo
            self.log_position = log_file.tell()

        # Formatar métricas no estilo `text/plain`
        metrics_output = []
        for (path, status), data in metrics.items():
            metrics_output.append(f"requests_total{{path=\"{path}\",status=\"{status}\"}} {data['total_requests']}")
            metrics_output.append(f"size_total{{path=\"{path}\",status=\"{status}\"}} {data['total_size']}")
            metrics_output.append(f"time_total{{path=\"{path}\",status=\"{status}\"}} {data['total_time']:.2f}")

        return "\n".join(metrics_output)
