import psutil

from app import app


class ProcessKit:

    @staticmethod
    def verify_if_process_running(process_search, is_process=True):
        # Se não for modo debug eu nao deixo executar os comandos
        if not app.config["DEBUG"]:
            return True

        count = 0
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                if "python" in p.name():
                    if len(p.cmdline()) > 1:
                        for cmd in p.cmdline():
                            if process_search in cmd:
                                count += 1
            except Exception as e:
                pass

        if is_process:
            if count >= 2:
                print("Desculpa, mas ja esta sendo executado...")
                return True
        else:
            if count >= 1:
                print("Desculpa, mas ja esta sendo executado...")
                return True

        return False