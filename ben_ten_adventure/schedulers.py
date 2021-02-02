class Task:
    """
    1 second = 20 ticks
    """

    def __init__(self):
        self.is_canceled = False
        self._id = 0

        self.is_delayed = False
        self.is_repeating = False
        self.is_delayed_repeating = False

    def on_run(self, current_tick) -> None:
        pass

    def on_cancel(self) -> None:
        """
        Helpfull when called TaskManager.shutdown.
        E.g. Your task is working with file, in this case you have time to save and close it.
        """
        pass


class RepeatingTask(Task):
    """
    Repeats task every `period` ticks. Runs while is_canceled is False.
    * I want to stop my task
        task_obj.is_canceled = True
    * I want my task to run only 600 ticks
        class MyCustomTask(RepeatingTask):
            def __init__(self, period):
                super().__init__(period)
                self.ticks_played = 0

        def on_run(self, current_tick):
            if self.ticks_played >= 600:
                self.is_canceled = True
                return
            ...
            code
            ...
            self.ticks_played += 1
    """

    def __init__(self, period):
        super().__init__()
        self.period = period
        self.is_repeating = True

    def on_run(self, current_tick):
        pass


class DelayedTask(Task):
    """
    DelayedTask.on_run is called only once after delay `self.delay`
    """

    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.is_delayed = True

    def on_run(self, current_tick):
        pass


class DelayedRepeatingTask(Task):
    """
    After delay of `delay` ticks will be running as normal RepeatingTask
    E.g. DelayedRepeatingTask(40, 20)
    After 40 ticks (= 2 seconds) will call on_run for the first time. 
    Than every 20 ticks (= 1 second) will be calling on_run. 
    As I said it's like RepeatingTask but with delay before start
    """

    def __init__(self, delay, period):
        super().__init__()
        self.delay = delay
        self.period = period

        self.is_delayed_repeating = True

    def on_run(self, current_tick):
        pass
