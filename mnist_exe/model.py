import tensorflow as tf
import numpy as np

def conv_layer(
    x,
    input_channels, 
    filter_height, 
    filter_width, 
    num_filters, 
    stride_y, 
    stride_x, 
    padding, 
    name):

    with tf.variable.scope(name):

        weights = tf.get_variable(
            name='weights', 
            shape=[filter_height, filter_width, input_channels, num_filters])

        biases = tf.get_variable(
            name='biases', 
            shape=[num_filters])
        
        conv = tf.nn.conv2d(
            input=x,
            filter=weights,
            strides=[1, stride_y, stride_x, 1], 
            padding=padding)

        bias = tf.nn.bias_add(
            value=conv, 
            bias=biases)

        relu = tf.nn.relu(
            features=bias)        

        return relu

def fc_layer(
    x,
    num_input,
    num_output, 
    name,
    is_relu):
    
    with tf.variable.scope(name):

        weights = tf.get_variable(
            name='weights', 
            shape=[num_input, num_output])

        biases = tf.get_variable(
            name='biases', 
            shape=[num_output])

        bias = tf.nn.wx_plus_b(
            x=x,
            weights=weights, 
            biases=biases)

        if is_relu:
            return tf.nn.relu(
                features=bias)
        else:
            return bias

def max_pool(
    x,
    filter_height,
    filter_width, 
    stride_y, 
    stride_x, 
    padding, 
    name):

    return tf.nn.max_pool(
        value=x, 
        ksize=[1, filter_height, filter_width, 1], 
        strides=[1, stride_y, stride_x, 1], 
        padding=padding, 
        name=name)

def dropout(
    x,
    keep_rate,
    is_train):
    
    return tf.cond(
        pred=is_train,
        true_fn=lambda: tf.dropout(
            x=x,
            keep_prob=keep_rate),
        false_fn=lambda: x)

def model(
    x,
    labels,
    train_mode):

    # Conv layer #1
    conv1 = conv_layer(
        x=x,
        input_channels=1, 
        filter_height=5, 
        filter_width=5, 
        num_filters=32, 
        stride_y=1, 
        stride_x=1, 
        padding='SAME', 
        name='conv1')

    # Pool layer #2
    pool2 = max_pool(
        x=conv1,
        filter_height=2,
        filter_width=2, 
        stride_y=2, 
        stride_x=2, 
        padding='VALID', 
        name='pool2')

    # Conv layer #3
    conv3 = conv_layer(
        x=pool2,
        input_channels=32, 
        filter_height=5, 
        filter_width=5, 
        num_filters=64, 
        stride_y=1, 
        stride_x=1, 
        padding='SAME', 
        name='conv3')

    # Pool layer #4
    pool4 = max_pool(
        x=conv3,
        filter_height=2,
        filter_width=2, 
        stride_y=2, 
        stride_x=2, 
        padding='VALID', 
        name='pool4')

    # Fc layer #5
    pool4_flat = tf.reshape(
        tensor=pool4,
        shape=[-1, 7 * 7 * 64])

    fc5 = fc_layer(
        x=pool4_flat,
        num_input=7 * 7 * 64,
        num_output=1024, 
        name='fc5',
        is_relu=True):

    drop = dropout(
        x=fc5,
        keep_rate=0.4,
        is_train=train_mode == 'TRAIN'):

    # Logit layer #6
    fc6 = fc_layer(
        x=drop,
        num_input=1024,
        num_output=10, 
        name='fc6',
        is_relu=False):

    predictions = {
        'classes': tf.argmax(
            input=fc6,
            axis=1),
        'probabilities': tf.nn.softmax(
            logits=fc6, 
            name='prob')
        }

         
