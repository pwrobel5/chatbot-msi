import functools

from chatterbot.logic import LogicAdapter


class CommonAdapter(LogicAdapter):
    """
    Abstract class for my common adapters

    :kwargs:
        * *positive* (``list``) --
          Questions related to adapter
        * *negative* (``list``) --
          Questions not related to adapter
        * *critical* (``list``) --
          List of keywords which cannot be in question related to adapter
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.positive = kwargs.get("positive", [])
        self.positive = list(map(lambda x: x.lower().split(":", 1)[0].split(), self.positive))
        self.positive = set(functools.reduce(lambda x, y: x + y, self.positive, []))

        self.negative = kwargs.get("negative", [])
        self.negative = list(map(lambda x: x.lower().split(":", 1)[0].split(), self.negative))
        self.negative = set(functools.reduce(lambda x, y: x + y, self.negative, []))

        self.critical = set(kwargs.get("critical", []))

    def can_process(self, statement):
        text = statement.text

        for critical_word in self.critical:
            if critical_word in text:
                return False

        return True

    def determine_confidence(self, statement):
        """
        :param statement: Statement object to calculate confidence of using current adapter
        :return: 0 if statement contains word from critical list
                 1 if number of words from positive is >= number of words from negative and is > 0
                 0 in other cases
        """

        text = statement.text.lower().split(":", 1)[0]

        for critical_word in self.critical:
            if critical_word in text:
                return 0

        positives_counter = functools.reduce(lambda counter, element: counter + 1 if element in text else counter,
                                             self.positive, 0)
        negatives_counter = functools.reduce(lambda counter, element: counter + 1 if element in text else counter,
                                             self.negative, 0)

        if positives_counter >= negatives_counter and positives_counter > 0:
            return 1
        else:
            return 0
