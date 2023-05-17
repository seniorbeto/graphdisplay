#include <stdio.h>
#include <math.h>

int* calculate_start_position(int* start_position, int* end_position, int radius) {
    int* result = (int*)malloc(sizeof(int)*2);

    int* center_position_start;
    center_position_start[0] = (start_position[0] + end_position[0]) / 2;
    center_position_start[1] = (start_position[1] + end_position[1]) / 2;

    int* center_position_end;
    center_position_end[0] = (end_position[0] + start_position[0]) / 2;
    center_position_end[1] = (end_position[1] + start_position[1]) / 2;

    int x1, y1, x2, y2;
    x1 = center_position_start[0];
    y1 = center_position_start[1];
    x2 = center_position_end[0];
    y2 = center_position_end[1];
    
    int x, y;
    x = x2 - x1;
    y = y2 - y1;

    float edge_angle = atan2(y, x);
    x = x1 + radius * cos(edge_angle);
    y = y1 + radius * sin(edge_angle);
    result[0] = x;
    result[1] = y;

    return result;

}

int* calculate_end_position(int* start_position, int* end_position, int radius){
    int* result = (int*)malloc(sizeof(int)*2);    

    int* center_position_start;
    center_position_start[0] = (start_position[0] + end_position[0]) / 2;
    center_position_start[1] = (start_position[1] + end_position[1]) / 2;

    int* center_position_end;
    center_position_end[0] = (end_position[0] + start_position[0]) / 2;
    center_position_end[1] = (end_position[1] + start_position[1]) / 2;

    int x1, y1, x2, y2;
    x1 = center_position_start[0];
    y1 = center_position_start[1];
    x2 = center_position_end[0];
    y2 = center_position_end[1];
    
    int x, y;
    x = x2 - x1;
    y = y2 - y1;

    float edge_angle = atan2(y, x);
    x = x1 - radius * cos(edge_angle);
    y = y1 - radius * sin(edge_angle);
    result[0] = x;
    result[1] = y;

    return result;
}
