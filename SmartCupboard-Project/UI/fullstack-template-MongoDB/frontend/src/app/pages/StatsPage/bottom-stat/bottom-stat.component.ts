import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ami-fullstack-bottom-stat',
  templateUrl: './bottom-stat.component.html',
  styleUrls: ['./bottom-stat.component.scss']
})

export class BottomStatComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }


  pressState = [true,false,false] ; 
  startButton = 0 ;

  public pressButtonFunc(buttonId : number){
    this.pressState[this.startButton] = false;
    this.startButton = buttonId;
    
    this.pressState[buttonId] = true;
  
  }
}