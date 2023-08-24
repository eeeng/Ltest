import torch
from torch import nn
from d2l import torch as d2l

net = nn.Sequential(
    # Burada nesneleri yakalamak için daha büyük bir 11 x 11'lik pencere kullanıyoruz.
    # Aynı zamanda, çıktının yüksekliğini ve genişliğini büyük ölçüde azaltmak
    # için 4'lük bir uzun adım kullanıyoruz. Burada, çıktı kanallarının sayısı
    # LeNet'tekinden çok daha fazladır.
    nn.Conv2d(1, 96, kernel_size=11, stride=4, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    # Evrişim penceresini küçült, girdi ve çıktı boyunca tutarlı yükseklik
    # ve genişlik için dolguyu 2'ye ayarlayın ve çıktı kanallarının sayısını artırın
    nn.Conv2d(96, 256, kernel_size=5, padding=2), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    # Ardışık üç evrişim katmanı ve daha küçük bir evrişim penceresi kullan.
    # Son evrişim katmanı dışında, çıktı kanallarının sayısı daha da artırılır.
    # Ortaklama katmanları, ilk iki evrişim katmanından sonra girdinin
    # yüksekliğini ve genişliğini azaltmak için kullanılmaz.
    nn.Conv2d(256, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nn.Flatten(),
    # Burada, tam bağlı katmanın çıktı sayısı, LeNet'tekinden birkaç kat
    # daha fazladır. Aşırı öğrenmeyi azaltmak için hattan düşürme katmanını kullan
    nn.Linear(6400, 4096), nn.ReLU(),
    nn.Dropout(p=0.5),
    nn.Linear(4096, 4096), nn.ReLU(),
    nn.Dropout(p=0.5),
    # Çıktı katmanı. Fashion-MNIST kullandığımız için sınıf sayısı
    # makaledeki gibi 1000 yerine 10'dur.
    nn.Linear(4096, 10))

X = torch.randn(1, 1, 224, 224)
for layer in net:
    X=layer(X)
    print(layer.__class__.__name__,'cikli sekli:\t',X.shape)

batch_size = 128
train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size, resize=224)

lr, num_epochs = 0.01, 10
d2l.train_ch6(net, train_iter, test_iter, num_epochs, lr, d2l.try_gpu())
