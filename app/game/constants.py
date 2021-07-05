# Статусы игры
ENDED_WITH_ERRORS = -2
CANCELLED_BY_OWNER = -1
NOT_STARTED = 0
STARTED = 1
HANDLING = 2
HANDLED = 3


def get_status(key: int) -> str:
    return {
        ENDED_WITH_ERRORS: "Завершено с ошибками",
        CANCELLED_BY_OWNER: "Отменено куратором",
        NOT_STARTED: "Не начато",
        STARTED: "Начато",
        HANDLING: "Обрабатывается",
        HANDLED: "Завершено",
    }[key]


# Режимы игры
CLASSIC = 0


def get_mode(key: int) -> str:
    return {
        CLASSIC: "Классический режим"
    }[key]
