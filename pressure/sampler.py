class SamplerConfig:
    def __init__(self):
        self.avg_size = 100
        self.avg_step = 50
        self.rt_size = 1000
        self.sample_limit = 0

    def validate(self):
        if (
            self.avg_size > 0
            and self.avg_step > 0
            and self.rt_size >= self.avg_size
            and self.avg_step <= self.avg_size
        ):
            return True
        else:
            return False


class Sampler:
    def __init__(self, config=None):
        if config is None:
            self.config = SamplerConfig()
        else:
            self.config = config
            if not SamplerConfig().validate():
                return f"sampler config is not valid {config}"

        self.samples = []
        self.rt_samples = []
        self.since_last_avg = 0

    def last_sample(self):
        return self.samples[-1] if self.samples else None

    def live_sample(self):
        if len(self.rt_samples) == 0:
            return None
        start = len(self.rt_samples) - self.config.avg_size
        if start < 0:
            start = 0
        return downsample(self.rt_samples[start:])

    def last_timestamp(self):
        return self.rt_samples[-1][0] if self.rt_samples else None

    def push(self, timestamp: int, sample: float):
        self.rt_samples.append([timestamp, sample])
        self.since_last_avg += 1
        self.do_avg()
        self.trim_samples()

    def push_batch(self, data):
        start_len = len(self.rt_samples)
        self.rt_samples.extend(data)
        delta = len(self.rt_samples) - start_len
        self.since_last_avg += delta
        self.do_avg()
        self.trim_samples()

    def remove_samples(self, before: int):
        new_samples = []
        for time, data in self.samples:
            if time >= before:
                new_samples.append([time, data])
        self.samples = new_samples

    def update_config(self, new: SamplerConfig):
        if not new.validate():
            return
        self.config = new

    def do_avg(self):
        while self.since_last_avg > self.config.avg_size:
            start = len(self.rt_samples) - self.since_last_avg
            samples = self.rt_samples[start : start + self.config.avg_size]
            self.samples.append([downsample(samples)])
            self.since_last_avg -= self.config.avg_step

    def trim_samples(self):
        if len(self.rt_samples) > self.config.rt_size:
            start = len(self.rt_samples) - self.config.rt_size
            del self.rt_samples[:start]

        if (
            self.config.sample_limit > 0
            and len(self.samples) > self.config.sample_limit
        ):
            start = len(self.samples) - self.config.sample_limit
            del self.rt_samples[:start]


def downsample(samples):
    ts = samples[len(samples) // 2][0]
    aval = sum(samples[i][1] for i in range(0, len(samples))) / len(samples)
    return ts, aval
