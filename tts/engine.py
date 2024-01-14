
class RemedeIPAToSpeechEngine:

    def __init__(self):
        ...

    def generate_audio(self, ipa: str) -> str:
        """
        Say :ipa:
        :param ipa: IPA text to say
        :return:
        """
        ssml = f"<phoneme alphabet=\"ipa\" ph=\"{ipa.replace('/', '')}\"></phoneme>"
        return ""
