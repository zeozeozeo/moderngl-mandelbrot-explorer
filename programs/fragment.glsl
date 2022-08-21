#version 430 core
out vec4 fragColor;
uniform vec2 window_size;
uniform float zoom;
uniform float max_iter;
uniform vec2 camera_pos;
uniform float MAX_ITERATIONS;

float mandelbrot(vec2 uv) {
    vec2 c = 5.0 * uv - vec2(0.7, 0.0);
    c = c / pow(zoom, 4.0) - camera_pos;
    vec2 z = vec2(0.0);
    for (float i = 0.0; i < max_iter; i++) {
        z = vec2(z.x * z.x - z.y * z.y,
                2.0 * z.x * z.y) + c;
        if (dot(z, z) > 4.0) return i / max_iter;
    }
    return 0.0;
}

vec3 hash13(float m) {
    float x = fract(sin(m) * 5625.246);
    float y = fract(sin(m + x) * 2216.486);
    float z = fract(sin(x + y) * 8276.352);
    return vec3(x, y, z);
}

void main(void) {
    vec2 uv = (gl_FragCoord.xy - 0.5 * window_size.xy) / window_size.y;
    vec3 col = vec3(0.0);

    float m = mandelbrot(uv);
    if (max_iter >= MAX_ITERATIONS) {
        col += hash13(m);
    } else {
        col += m;
        col = pow(col, vec3(0.4545));
    }
    
    fragColor = vec4(col, 1.0);
}
