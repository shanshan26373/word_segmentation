#ifndef WEBVAD_H
#define WEBVAD_H

#include <QObject>
#include <QUrl>

class WebVAD : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QList<int> result READ result WRITE setResult NOTIFY resultChanged)
public:
    explicit WebVAD(QObject *parent = nullptr);
    QList<int> result();
    void setResult(QList<int>);

    Q_INVOKABLE void process(QUrl);

private:
    QList<int> m_result;

signals:
    void resultChanged();

};

#endif // WEBVAD_H
