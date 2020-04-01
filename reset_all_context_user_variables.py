from requests import Session
from uuid import uuid4
from json import load

# Fill with bot authorization key and user identity
BOT_AUTHORIZATION = ''
USER_IDENTITY = ''

COMMANDS_URL = 'https://msging.net/commands'
DELETE_METHOD = 'delete'
GET_METHOD = 'get'

if BOT_AUTHORIZATION == '' or USER_IDENTITY == '':
    print(
        '[ERROR] Reason: : must have a valid bot_authorization key and user_identity.'
    )
    exit(-1)


def create_all_context_request():
    return {
        'id': str(uuid4()),
        'method': GET_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}'
    }


def delete_specific_context_variable(context_var):
    return {
        'id': str(uuid4()),
        'method': DELETE_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}/{context_var}'
    }


if __name__ == "__main__":
    session = Session()
    session.headers = {
        'Authorization': BOT_AUTHORIZATION
    }
    cmd_body_context = create_all_context_request()

    cmd_res_context = session.post(COMMANDS_URL, json=cmd_body_context)

    if cmd_res_context.status_code == 200:
        cmd_res_context = cmd_res_context.json()

        if cmd_res_context['status'] == 'success':

            for context_var in cmd_res_context['resource']['items']:
                cmd_body_delete_context = delete_specific_context_variable(
                    context_var)
                cmd_res_delete_context = session.post(
                    COMMANDS_URL, json=cmd_body_delete_context)

                if cmd_res_delete_context.status_code == 200:
                    cmd_res_delete_context = cmd_res_delete_context.json()
                    if cmd_res_delete_context['status'] == 'success':
                        print(f'Deleted context var :{context_var}')
                else:
                    print(
                        f'[ERROR] Reason: {cmd_res_delete_context["reason"]["description"]}'
                    )
        else:
            print(
                f'[ERROR] Reason: {cmd_res_context["reason"]["description"]}'
            )
    else:
        cmd_res_context = cmd_res_context.json()
        print(
            f'[ERROR] Reason: {cmd_res_context["description"]}'
        )
    print('Finished')
