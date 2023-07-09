import numpy as np
import tensorflow as tf
import Mining as mi

period = 100

file_name = 'Datas\\Answers_2021.csv'
datas = mi.answers_writer(file_name , period)
x = datas[0]
y = datas[1]

file_name = 'Datas\\Answers_2020.csv'
test_datas = mi.answers_writer(file_name , period)
test_x = np.array([test_datas[0][0], test_datas[0][1000], test_datas[0][2000]])
#test_x = np.array([[0,1,2,3], [12,15,18,21], [79,66,54,41]])
test_y = [test_datas[1][0], test_datas[1][1000], test_datas[1][2000]]



model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation = 'relu'),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dense(1, activation = 'sigmoid'),
])

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

model.fit( x, y, epochs = 100)

model.save('my_model.h5')

print(model.predict(test_x))
print(test_y)
