from rest_framework import status, viewsets
from rest_framework.response import Response
from project.util import get_languages, interpretor, detect_lang, get_text


class LanguageViewset(viewsets.ModelViewSet):
    def get_languages(self, request):
        lang_type = self.request.query_params.get('lang_type', None)
        if lang_type is not None:
            lang, count = get_languages(lang_type.lower())
            response_dict = dict()
            response_dict['total'] = count
            response_dict['languages'] = lang
            if lang:
                return Response(data=response_dict, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': 'Invalid language type.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'Requires language type.'}, status=status.HTTP_400_BAD_REQUEST)

    def translate(self, request):
        data = request.data
        try:
            dest_lang = data['output_language'].lower()
            input_text = data['text']
        except:
            return Response(data={'message': 'Parameter(s) missing.'}, status=status.HTTP_400_BAD_REQUEST)
        src_lang = None if 'input_language' not in data else data['input_language'].lower()
        response_text, dest_language, src_language = interpretor(input_text, dest_lang, src_lang)
        if response_text:
            return Response(data=response_text, status=status.HTTP_200_OK)
        else:
            if dest_language == 0:
                wrong_entry = 'output language'
            elif src_language == 0:
                wrong_entry = 'input language'
            else:
                wrong_entry = 'both input and output languages'
            return Response(data={'message': 'Invalid entry for {}.'.format(wrong_entry)},
                            status=status.HTTP_400_BAD_REQUEST)

    def detect_language(self, request):
        file_type = self.request.query_params.get('file_type', None)
        if file_type is None:
            return Response(data={'message': 'Requires file type.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            if file_type.lower() == 'file':
                try:
                    input_file_path = data['input']
                    file_format = self.request.query_params.get('file_format', None)
                    input_text = get_text(input_file_path, file_format)
                    if input_text == 0:
                        return Response(data={'message': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={'message': 'Input is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            elif file_type.lower() == 'text':
                try:
                    input_text = data['input']
                except:
                    return Response(data={'message': 'Input is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'message': 'Invalid file type.'}, status=status.HTTP_400_BAD_REQUEST)

        language, accuracy = detect_lang(input_text)
        response_dict = dict()
        response_dict['language'] = language
        response_dict['accuracy'] = accuracy
        return Response(data=response_dict, status=status.HTTP_200_OK)
