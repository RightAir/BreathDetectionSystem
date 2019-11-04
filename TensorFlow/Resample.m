clc, clear

flow = readmatrix('flowTraining.csv');
sensor = readmatrix('training.csv');

%%

sensor_1 = sensor(:, 2);
sensor_2 = sensor(:, 3);
sensor_3 = sensor(:, 4);
sensor_4 = sensor(:, 5);
sensor_5 = sensor(:, 6);
sensor_6 = sensor(:, 7);
sensor_7 = sensor(:, 8);
sensor_8 = sensor(:, 9);

flow_undersampled = resample(flow, length(sensor_1), length(flow));

range = (1:9000);

figure
plot(range, flow_undersampled, range, sensor_1)