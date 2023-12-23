from random import choice

from form_dataclasses import *


DATA_SCIENCE_IMAGE_LINK = 'https://imgbly.com/ib/urP1UeXc72'
MACHINE_LEARNING_IMAGE_LINK = 'https://imgbly.com/ib/zvxWV1Dfn1'
QA_IMAGE_LINK = 'https://imgbly.com/ib/bQsjJqvFt4'
WEB_IMAGE_LINK = 'https://imgbly.com/ib/g1EjZaWvdX'
BOTS_IMAGE_LINK = 'https://imgbly.com/ib/JT6Uq8kVhv'
ALL_IMAGE_LINK = 'https://imgbly.com/ib/hvGDaxWhnP'


def python_developer_form_calculate_result(weights: Weights) -> tuple[str, str]:

    weights.complexity //= 2  # due to the maximum possible value, it is 2 times larger than other weights

    if weights.complexity == weights.beauty == weights.development_speed:
        return 'Я не знаю, как ты это сделал, но по ответам могу сказать, что тебе подойдёт ВСЁ', ALL_IMAGE_LINK

    elif weights.complexity > weights.beauty and weights.complexity > weights.development_speed:

        if weights.beauty == weights.development_speed:
            return (
                'Тут либо data science, либо machine learning, на этом мои полномочия всё',
                choice((DATA_SCIENCE_IMAGE_LINK, MACHINE_LEARNING_IMAGE_LINK))
            )

        elif weights.beauty > weights.development_speed:
            return (
                'Ты, судя по ответам, крайне хорош, рекомендую тебе data science, тут и красивенькие графики и сложна',
                DATA_SCIENCE_IMAGE_LINK
            )

        else:
            return 'А ты умён, рекомендую machine learning и всё вот это вот', MACHINE_LEARNING_IMAGE_LINK

    elif weights.development_speed > weights.complexity and weights.development_speed > weights.beauty:

        if weights.complexity == weights.beauty:
            return (
                'Тебе должны подойти тестирование и разработка различных ботов (telegram, discord, ...)',
                choice((QA_IMAGE_LINK, BOTS_IMAGE_LINK))
            )

        elif weights.complexity > weights.beauty:
            return 'Попробуй тестирование различных программ и сайтов', QA_IMAGE_LINK

        else:
            return 'Ответственно рекомендую тебе заняться разработкой ботов (telegram, discrod, ...)', BOTS_IMAGE_LINK

    else:

        if weights.development_speed == weights.complexity:
            return (
                'Рекомендую попробовать разработку ботов или web development', choice((BOTS_IMAGE_LINK, WEB_IMAGE_LINK))
            )

        elif weights.development_speed > weights.complexity:
            return 'Попробуй разработку ботов', BOTS_IMAGE_LINK

        else:
            return 'Рекомендую web и всё, что с ним связано', WEB_IMAGE_LINK


PythonDeveloperForm = Form(
    title='Какой ты python-разработчик?',
    questions=[
        Question(
            text='Сколько ты изучаешь python?',
            answers=[
                Answer(text='Я новичок (до 3 месяцев)', weights=Weights(complexity=-5, development_speed=5)),
                Answer(text='Что-то уже понимаю (от 3 до 12 месяцев', weights=Weights()),
                Answer(text='Шарю (от 12 месяцев)', weights=Weights(complexity=5)),
            ],
        ),
        Question(
            text='Как ты относишься к PEP-8?',
            answers=[
                Answer(text='Не ведаю что это за лошадка такая', weights=Weights(complexity=-5, development_speed=5)),
                Answer(text='Стараюсь придерживаться', weights=Weights(complexity=5)),
                Answer(text='Боготворю', weights=Weights(complexity=10)),
            ],
        ),
        Question(
            text='Любишь ли ты "наводить красоту" для конечного пользователя (делать красивый интерфейс)?',
            answers=[
                Answer(
                    text='Не, все же умеют работать с консолью и понимать мои мысли с полуслова',
                    weights=Weights(complexity=-5, development_speed=5, beauty=-10),
                ),
                Answer(text='Ну, сносный UI могу накидать', weights=Weights(beauty=5)),
                Answer(text='Обожаю доводить всё, что видит пользователь, до идеала', weights=Weights(beauty=15)),
            ],
        ),
        Question(
            text='Как ты относишься к страданиям?',
            answers=[
                Answer(text='Не, это не моё', weights=Weights(complexity=-10)),
                Answer(text='Всё хорошо в меру', weights=Weights(complexity=5)),
                Answer(text='Как к смыслу жизни', weights=Weights(complexity=15, development_speed=-10)),
            ],
        ),
        Question(
            text='Вывод программы должен быть?',
            answers=[
                Answer(text='Предельно простой, сугубо информативный', weights=Weights(beauty=-10)),
                Answer(text='Хоть чуть-чуть марафета нужно навести всегда', weights=Weights(beauty=5)),
                Answer(
                    text='Неотразим, человек обязан восхищаться увиденным минимум в течение суток',
                    weights=Weights(beauty=15, development_speed=-10),
                ),
            ],
        ),
        Question(
            text='Любишь разбираться в чужом коде?',
            answers=[
                Answer(text='Неееее, они же пишут как черти', weights=Weights(complexity=-5, development_speed=5)),
                Answer(text='Могу, но стараюсь этого избегать', weights=Weights(complexity=5)),
                Answer(text='Обожаю, они же пишут как черти', weights=Weights(complexity=10)),
            ],
        ),
        Question(
            text='Do you speak English?',
            answers=[
                Answer(text='Оф корз, вэри велл', weights=Weights(complexity=-5)),
                Answer(text='Yeah, but not a master', weights=Weights(complexity=5)),
                Answer(
                    text='This is my life, this is a wonderful world of information', weights=Weights(complexity=10)
                ),
            ],
        ),
        Question(
            text='Любишь делать БОЛЬШИЕ проекты?',
            answers=[
                Answer(text='Это сложнаа, не очень люблю', weights=Weights(complexity=-5, development_speed=10)),
                Answer(text='Почему бы и нет', weights=Weights(complexity=5, development_speed=-5)),
                Answer(
                    text='Обожаю делать большие проекты, засеть на пару месяцев над чем-то одним - чистый кайф',
                    weights=Weights(complexity=10, development_speed=-10),
                ),
            ],
        ),
    ],
    calculate_result=python_developer_form_calculate_result,
)
