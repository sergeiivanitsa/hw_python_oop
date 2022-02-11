class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.get_distance() / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите калории в %s.' %
                                  (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        run_calories: float = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             - self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR)
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    MIN_IN_HOUR: int = 60

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.CALORIES_MEAN_SPEED_SHIFT * self.weight) * self.duration
            * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                        / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                           * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in read:
        result = read[workout_type](*data)
        return result


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
