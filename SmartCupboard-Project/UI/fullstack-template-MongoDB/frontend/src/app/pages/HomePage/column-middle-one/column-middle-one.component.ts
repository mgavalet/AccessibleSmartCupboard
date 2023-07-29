import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'ami-fullstack-column-middle-one',
  templateUrl: './column-middle-one.component.html',
  styleUrls: ['./column-middle-one.component.scss']
})
export class ColumnMiddleOneComponent implements OnInit {

  
  @Input() mariosData : any ;
  
  constructor() { }

  ngOnInit() {
  }

}
