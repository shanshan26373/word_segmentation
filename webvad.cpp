
#include "webvad.h"
#include "qdebug.h"
#include "qfileinfo.h"
#include "webrtc/webrtc.hpp"
#include "AudioFile.h"
#include <iostream>
#include <QDir>

WebVAD::WebVAD(QObject *parent)
    : QObject{parent}
{

}

QList<int> WebVAD::result()
{
    return m_result;
}

void WebVAD::setResult(QList<int> l)
{
    if(m_result != l)
    {
        m_result = l;
        emit resultChanged();
    }
}

void WebVAD::process(QUrl path)
{
    QString str = path.toString(QUrl::RemoveScheme).remove(0, 3);
    QFileInfo FI(str);
    QString dirPath = FI.canonicalPath();
    QString baseName = FI.baseName();
    QString savePath = dirPath + "/" + baseName + ".bak.wav";

    AudioFile<qreal> file;
    file.load(savePath.toLocal8Bit().toStdString());
    qDebug() << str;

    QDir dir(dirPath);
    QStringList wavFiles = dir.entryList(QStringList() << "*.wav", QDir::Files);
    m_result.clear();

    for (const QString& wavFile : wavFiles) {
        QString filePath = dirPath + "/" + wavFile;
        FILE* f;
        char buf[320];
        size_t nread;
        webrtc::Vad vad(webrtc::Vad::kVadAggressive);

        bool ret = vad.Init();
        if(ret == false)
        {
            qDebug() << "Failed";
            return;
        }
        f = std::fopen(filePath.toLocal8Bit().toStdString().c_str(), "rb");
        std::fseek(f, 44, SEEK_SET);

        while (!feof(f)) {
            nread = fread(buf, 1, sizeof(buf), f);
            if (nread != 320) {
                printf("0\n");
                break;
            }

            int ret = vad.IsSpeech(reinterpret_cast<int16_t*>(buf), 80, file.getSampleRate());
            if (ret == webrtc::Vad::kError) {
                printf("vad process failed");
                break;
            }
            m_result.append(ret > 0 ? 1 : 0);
        }

        fclose(f);
        qDebug() << "Processed file: " << filePath;
    }

    emit resultChanged();
    qDebug() << "Exit successful";
}