def fit(model, data_bunch, callbacks, batch_size, epochs, class_weight=None, return_best_model=False,
        custom_objects=None):

    """
    Fits a Keras model when using arrays as inputs

    :param model: A (compiled) Keras model
    :param DataBunch data_bunch: A DataBunch consisting of "train" and "valid" DataSets
    :param dict callbacks: The Keras callbacks to perform during training
    :param int batch_size: The batch size to use during training
    :param int epochs: The number of Epochs to train for
    :param dict class_weight: Class weights to be applied during training
    :param bool return_best_model: If set to true, instead of return the model from the final epoch, the model with the
    best accuracy will be returned
    :param custom_objects: Any custom objects with which a best model may have been saved (custom loss functions would count
    as custom objects)
    :return: A (fitted) Keras model, the training history
    """

    train_x = data_bunch.train.features.underlying
    train_y = data_bunch.train.targets.underlying
    valid_x = data_bunch.valid.features.underlying
    valid_y = data_bunch.valid.targets.underlying

    history = model.fit(x=train_x,
                        y=train_y,
                        validation_data=(valid_x,valid_y),
                        batch_size=batch_size,
                        epochs=epochs,
                        class_weight=class_weight,
                        callbacks=callbacks
                        )


    if return_best_model:
        # by default Keras returns the model from the last epoch
        from keras.models import load_model
        model = load_model(__get_model_checkpoint(callbacks).filepath,
                           custom_objects=custom_objects)

    return model, history


def fit_generator(model, data_bunch, callbacks, epochs, class_weight=None, return_best_model=False,
        custom_objects=None):

    """
    Fits a Keras model when using generators as input

    :param model: A (compiled) Keras model
    :param DataBunch data_bunch: A DataBunch consisting of "train" and "valid" DataSets
    :param dict callbacks: The Keras callbacks to perform during training
    :param int batch_size: The batch size to use during training
    :param int epochs: The number of Epochs to train for
    :param dict class_weight: Class weights to be applied during training
    :param bool return_best_model: If set to true, instead of return the model from the final epoch, the model with the
    best accuracy will be returned
    :param custom_objects: Any custom objects with which a best model may have been saved (custom loss functions would count
    as custom objects)
    :return: A (fitted) Keras model, the training history
    """

    train_iterator = data_bunch.train.features.underlying
    valid_iterator = data_bunch.valid.features.underlying

    history = model.fit_generator(generator=train_iterator,
                                  validation_data=valid_iterator,
                                  steps_per_epoch= train_iterator.n // train_iterator.batch_size,
                                  validation_steps= valid_iterator.n // valid_iterator.batch_size,
                                  epochs=epochs,
                                  class_weight=class_weight,
                                  callbacks=callbacks
                                  )

    if return_best_model:
        # by default Keras returns the model from the last epoch
        from keras.models import load_model
        model = load_model(__get_model_checkpoint(callbacks).filepath,
                           custom_objects=custom_objects)

    return model, history


def __get_model_checkpoint(callbacks):
    return [callback for callback in callbacks if callback.__class__.__name__=="ModelCheckpointProvider"][0]