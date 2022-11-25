# le4-audio-kuis (private)

京都大学 工学部 情報学科 計算機科学実験及演習4 音響信号処理 のサンプルソースコードです。

簡易カラオケシステムを作成します。

## Files
- `plot_waveform.py`: 波形の表示
- `plot_spectrum.py`: スペクトルの図示

## usage of SOX
- 録音：`sox -r 16k -b 16 -c 1 -d output.wav trim 0 10`
- 再生：`sox input.wav -d`