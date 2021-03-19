/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.project;

/**
 *
 * @author Owais
 */
public class Board {
    //saves position in array with 0 as null and numbers as the number at that position
    private int[] board = new int[16];
    boolean game=true;
    public Board(){
        //initialize blank board
        for(int i=0; i<16;i++){
            board[i]=0;
        }
    }
    public int[] getBoard(){
        return this.board;
    }
    public void setBoard(int[] b){
        this.board=b;
    }
    public void gameOver(){
        this.game=false;
    }
    public boolean gameOn(){
        return this.game;
    }
}
