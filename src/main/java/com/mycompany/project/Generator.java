/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.project;

import java.util.ArrayList;
import java.util.Random;

/**
 *
 * @author Owais
 */
public class Generator extends Board {

    Board b;

    //new tile generator:
    //generate random empty position 0-16 and number either 4 or 2
    public Generator(Board b) {
        this.b = b;
        //generate board with 2 random pieces
        addTile();
        addTile();
    }

    private int rng(int min, int max) {
        Random r = new Random();
        return r.nextInt((max - min) + 1) + min;
    }

    public void addTile() {
        //make list of empty locations (val=0)
        ArrayList<Integer> empty = new ArrayList<Integer>();
        int[] board = b.getBoard();
        for (int i = 0; i < 16; i++) {
            if (board[i] == 0) {
                empty.add(i);
            }
        }
        //pick out a random location to add tile
        int s = empty.size();
        if (s != 0) {
            int index = empty.get(rng(0, s - 1));
            //add either 2 or 4, at random
            int value = rng(0, 1);
            if (value == 0) {
                //2
                board[index] = 2;
            } else {
                //4
                board[index] = 4;
            }
            //return array with added element
            b.setBoard(board);
        } else {
            b.gameOver();
        }
    }

    public int swipe(String dir) {
        /*
        0   1   2   3   
        4   5   6   7     
        8   9   10  11  
        12  13  14  15  
    if b0!=0 && b4!=0 && b0==b4, b0=b0*2,b4=b8,b8=b12,b12=0.
    if b4!=0 && b8!=0 && b4==b8, b4==b4*2, b8=b12
         */
        int[] a = this.b.getBoard();
        boolean moved=false;
        switch (dir) {
            case "up" -> {
                ArrayList<Integer> B = new ArrayList<>();
                //add together the pairs

                for (int i = 0; i < 4; i++) {
                    for (int j = 0; j <= 12; j += 4) {
                        if (a[i + j] != 0) {
                            B.add(a[i + j]);
                        }
                    }
                    int l = 0;
                    while (!B.isEmpty()) {
                        //remove first entry  and put it into b array
                        int index = 0;
                        a[l + i] = B.get(index);
                        B.remove(index);
                        l += 4;
                    }
                    while (l <= 12) {
                        a[l + i] = 0;
                        l += 4;
                        moved = true;
                    }
                }
            }
            case "left" -> {
                ArrayList<Integer> B = new ArrayList<>();
                //add together the pairs

                for (int j = 0; j <= 12; j += 4) {
                    for (int i = 0; i < 4; i++) {
                        if (a[i + j] != 0) {
                            B.add(a[i + j]);
                        }
                    }
                    int l = 0;
                    while (!B.isEmpty()) {
                        //remove first entry  and put it into b array
                        int index = 0;
                        a[l + j] = B.get(index);
                        B.remove(index);
                        l++;
                    }
                    while (l < 4) {
                        a[l + j] = 0;
                        l++;
                        moved = true;
                    }
                }
            }
            case "right" -> {
                ArrayList<Integer> B = new ArrayList<>();
                //add together the pairs

                for (int j = 0; j <= 12; j += 4) {
                    for (int i = 0; i < 4; i++) {
                        if (a[i + j] != 0) {
                            B.add(a[i + j]);
                        }
                    }
                    int l = 3;
                    while (!B.isEmpty()) {
                        //remove first entry  and put it into b array
                        int index = B.size() - 1;
                        a[l + j] = B.get(index);
                        B.remove(index);
                        l--;
                    }
                    while (l >= 0) {
                        a[l + j] = 0;
                        l--;
                        moved = true;
                    }
                }
            }
            case "down" -> {
                ArrayList<Integer> B = new ArrayList<>();
                //add together the pairs

                for (int i = 0; i < 4; i++) {
                    for (int j = 12; j >= 0; j -= 4) {
                        if (a[i + j] != 0) {

                            B.add(a[i + j]);
                        }
                    }
                    int l = 12;
                    while (!B.isEmpty()) {
                        //remove first entry  and put it into b array
                        int index = 0;
                        a[l + i] = B.get(index);
                        B.remove(index);
                        l -= 4;
                    }
                    while (l >= 0) {
                        a[l + i] = 0;
                        l -= 4;
                        moved = true;
                    }
                }

            }
        }

        if (moved) {
//set the board and return 1
            this.b.setBoard(a);
            return 1;
        }

        //if there are no changes return 0 changes
        return 0;
    }

}
