# CPEN513 A1 Routing

## Run the program

run the animation.py

```
cd routing
python animation
```

inside the file, you can specify the benchmark file and also the routing function.

1. benchmark file 

   put filename as the first argument or specify it inside the file

   ```
   line 17: filename = "temp"
   ```

   

2. routing function

   `frame = $routing function$`

   ```
   line 181:
   	ani = animation.FuncAnimation(fig, update_anim,
       init_func=init_anim, frames=route_with_shuffle(10),
       repeat=False, interval=100, save_count=200)
   ```

   

## Test

`Pytest` is used here



run the `route_test.py` file with `pytest` under the routing directory

```
cd routing
python -m pytest route_test.py
```

## Gif results

1. example
   ![example](README.assets/example.png)
   ![example](README.assets/example.gif)

2. impossible
   ![impossible](README.assets/impossible.png)
   ![impossible](README.assets/impossible-1612438509268.gif)

   

3. impossible2
   ![impossible2](README.assets/impossible2.png)
   ![impossible2](README.assets/impossible2-1612438540383.gif)

   

4. kuma
   ![kuma](README.assets/kuma.png)
   ![kuma](README.assets/kuma.gif)

5. misty
   ![misty](README.assets/misty.png)
   ![misty](README.assets/misty.gif)

6. oswald
   ![oswald](README.assets/oswald.png)
   ![oswald](README.assets/oswald.gif)

7. rusty

   ![rusty](README.assets/rusty.png)
   ![rusty](README.assets/rusty.gif)

8. stanley

   ![stanley](README.assets/stanley.png)
   ![stanley](README.assets/stanley.gif)

9. stdcell

   ![stdcell](README.assets/stdcell.png)
   ![stdcell](README.assets/stdcell.gif)

10. sydney
    ![sydney](README.assets/sydney.png)
    ![sydney](README.assets/sydney.gif)

11. temp
    ![temp](README.assets/temp.png)
    ![temp](README.assets/temp.gif)

12. wavy
    ![wavy](README.assets/wavy.png)
    ![wavy](README.assets/wavy.gif)