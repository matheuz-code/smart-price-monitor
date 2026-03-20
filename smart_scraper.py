import schedule
import time

from agent import executar_agente


schedule.every(2).minutes.do(executar_agente)

print("Agente iniciado... aguardando tarefas.")

while True:

    schedule.run_pending()

    time.sleep(1)