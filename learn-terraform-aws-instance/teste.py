import os

# salvar resultado do comando em uma variável
result = os.popen("terraform output aws_iam_users").read()

print("ESSES SÂO OS USERS: ", result)