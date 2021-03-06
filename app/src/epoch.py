import numpy as np
from chainer import Variable, using_config


# train model in each epoch
def training_epoch(i, cim, model, optimizer, batchsize=100):
    x_batch = Variable(cim.get_x_training_batch(i, batchsize))
    t_batch = Variable(cim.get_t_training_batch(i, batchsize))

    model.zerograds()
    loss, acc = model(x_batch, t_batch)
    loss.backward()
    optimizer.update()

    return loss.data, acc.data


# test accuracy in each epoch
def testing_epoch(i, cim, model, batchsize=100):
    x_batch = Variable(cim.get_x_testing_batch(i, batchsize))
    t_batch = Variable(cim.get_t_testing_batch(i, batchsize))
    with using_config('train', False):
        _, acc = model(x_batch, t_batch)

    return acc.data


# infer images through classifiers
def infer_epoch(model, x_batch):
    x_batch_t = Variable(x_batch)
    with using_config('train', False):
        x_infer_t = model.forward(x_batch_t)
    x_infer_t = np.argmax(x_infer_t.data, axis=1)
    x_infer = x_infer_t.astype(np.int)

    return x_infer
