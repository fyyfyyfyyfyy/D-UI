import sherpa_ncnn  # type: ignore
import sounddevice as sd  # type: ignore


def get_asr_response() -> str:
    devices = sd.query_devices()
    default_input_device_idx = sd.default.device[0]
    print(f'Use default device: {devices[default_input_device_idx]["name"]}')
    recognizer = sherpa_ncnn.Recognizer(
        tokens="./ncnn/tokens.txt",
        encoder_param="./ncnn/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin="./ncnn/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param="./ncnn/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin="./ncnn/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param="./ncnn/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin="./ncnn/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    sample_rate = recognizer.sample_rate
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
    last_result = ""

    audio_res = []

    i = 0

    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)  # a blocking read
            audio_res.append(samples)
            samples = samples.reshape(-1)
            recognizer.accept_waveform(sample_rate, samples)
            result = recognizer.text
            i += 1

            # 通过调节数字控制时间（不精准）
            # 逻辑：没有读取到语音并且过去5秒->结束；读取到语音并且过去2秒->结束
            if i == 50 and not result:
                break
            elif i == 20 and result:
                break

            if last_result != result:
                i = 0
                last_result = result
                print("\r{}".format(result), end="", flush=True)

    return result


def wait_and_get_asr_response():
    input('Press Enter To Wake Up:')
    return get_asr_response()
