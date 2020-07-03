from blip_session import BlipSession
import sys
import json

BOT_AUTHORIZATION = ''
USER_IDENTITY = ''

GET_METHOD = 'get'
TYPE_TEXT = 'text/plain'

if BOT_AUTHORIZATION == '' or USER_IDENTITY == '':
    print(
        '[ERROR] Reason: : must have a valid bot_authorization key and USER_IDENTITY.'
    )
    exit(-1)


def create_all_context_request():
    return {
        'method': GET_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}'
    }


def get_specific_data_context_request(context_var):
    return {
        'method': GET_METHOD,
        'to': 'postmaster@msging.net',
        'uri': f'/contexts/{USER_IDENTITY}/{context_var}'
    }


if __name__ == "__main__":
    blipSession = BlipSession(BOT_AUTHORIZATION)
    res_context = blipSession.process_command(create_all_context_request())
    jsonResponse = {}

    if (res_context.get('status') == 'success'):
        for context_var in res_context['resource']['items']:
            res__get_data_context = blipSession.process_command(
                get_specific_data_context_request(context_var))
            if res__get_data_context['status'] == 'success':
                data_var = res__get_data_context['resource'].encode(
                    'utf-8').decode('utf-8')
                jsonResponse[context_var] = data_var

        print(json.dumps(jsonResponse, ensure_ascii=False))
        print('Finished')
        exit(-1)
    if (res_context.get('status') == 'failure'):
        print(
            f'[ERROR] Reason: {res_context["reason"]["description"]}\nFinished'
        )
    else:
        print(
            f'[ERROR] Reason: {res_context["description"]}\nFinished'
        )
