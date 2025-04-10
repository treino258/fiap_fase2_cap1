from src.database.tipos_base.model import Model
from src.database.utils import input_bool, input_int
from src.logger.loggers import log_warning, log_info, log_error, log_success
from datetime import datetime
import json
import os

from src.settings import IMPORTS_DIR


def importar_json_generico(
    model: type[Model],
):

    log_info(f"Iniciando a importação de dados para a tabela de {model.display_name_plural()}")

    #verifica os arquivos no diretório de importação

    arquivos = os.listdir(IMPORTS_DIR)

    arquivos_json = list(filter(lambda x: x.endswith('.json'), arquivos))

    if len(arquivos_json) == 0:
        log_warning(f"Nenhum arquivo encontrado no diretório de importação {IMPORTS_DIR}")
        return

    log_info(f"Arquivos encontrados no diretório de importação: {len(arquivos_json)}")

    for i, file in enumerate(arquivos_json):
        print(f"{i+1}) {file}")

    print()

    escolha = None

    while escolha is None:
        try:
            escolha = input_int('Arquivo importar', message_override='Escolha o arquivo para importar ou 0 para voltar: ')
        except ValueError as e:
            log_warning(str(e))
            escolha = None

        match escolha:
            case 0:
                log_info("Operação cancelada pelo usuário")
                return
            case _:
                if escolha > len(arquivos_json):
                    log_warning(f"Escolha inválida. Escolha um número entre 1 e {len(arquivos_json)}")
                    escolha = None

    arquivo_target = arquivos_json[escolha-1]

    with open(os.path.join(IMPORTS_DIR, arquivo_target), 'r', encoding='utf-8') as file:
        data_string = file.read()
        data = json.loads(data_string)

    instances = []

    if isinstance(data, dict):
        try:
            instance = model.from_dict(data)
            instances.append(instance)
        except Exception as e:
            exemplo = model.exemple_instance()
            log_error(f"Erro ao importar o arquivo {arquivo_target}: {e}\nVerifique se o arquivo está no formato correto.\nExemplo de instância: {exemplo.to_json()}")
            return

    elif isinstance(data, list):
        for i, item in enumerate(data):
            try:
                instance = model.from_dict(item)
                instances.append(instance)
            except Exception as e:
                exemplo = model.exemple_instance()
                log_error(f"Erro ao importar o arquivo {arquivo_target}: {e}\nVerifique se o arquivo está no formato correto.\nExemplo de instância: [\n{exemplo.to_json()}\n...\n]")
                return
    else:
        exemplo = model.exemple_instance()
        log_error(f"Erro ao importar o arquivo {arquivo_target}: o arquivo não está no formato JSON válido.\nVerifique se o arquivo está no formato correto.\nExemplo de instância: [\n{exemplo.to_json()}\n...\n]")
        return

    if len(instances) == 0:
        log_warning(f"Nenhuma instância encontrada no arquivo {arquivo_target}")
        return

    instances_no_id = []

    for i in instances:
        instances_no_id.append(i.copy_with({'id': None}))

    log_info("Arquivo importado com sucesso!")

    dataframe = model.get_dataframes(instances_no_id)

    print()
    print(dataframe)
    print()
    print(f"Deseja salvar as instâncias de {model.display_name()} na database?")
    salvar = input_bool("Salvar", modo="S")

    if not salvar:
        log_info("Operação cancelada pelo usuário")
        return

    log_info("Salvando instâncias na database...")

    has_error = False
    has_sucess = False
    for instance in instances_no_id:
        try:
            instance.save()
            has_sucess = True
        except Exception as e:
            log_error(f"Erro ao salvar a instância {instance} na database: {e}")
            has_error = True
            continue

    if has_error:
        log_warning(f"Algumas instâncias não foram salvas na database. Verifique os logs para mais detalhes.")

    if not has_sucess:
        log_error(f"Nenhuma instância foi salva na database.")
        return

    log_success(f"Instâncias de {model.display_name()} salvas na database com sucesso!")

