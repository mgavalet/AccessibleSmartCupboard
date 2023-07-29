import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {HomeComponent} from './pages/HomePage/home/home.component';
import {ProductPageComponent} from './pages/ProductPage/product-page/product-page.component'; 
import {StatMainComponent} from './pages/StatsPage/stat-main/stat-main.component' ; 
import {DisplayCupboardsPageComponent} from './pages/DisplayCupboardspage/display-cupboards-page.component' ;
import {AmiPageComponent} from './pages/AmiPage/ami-page.component' ;
import {ModeratorPageComponent} from './pages/ModeratorPage/moderator-page.component' ;

const routes: Routes = [
  { path: 'home', loadChildren: () => import('./pages/HomePage/home/home.module').then(m => m.HomeModule) },
  {path : '' , component : HomeComponent}, 
  {path : 'ProductPage' , component : ProductPageComponent},
  {path : 'StatisticsPage' , component : StatMainComponent},
  {path: 'DisplayCupboards' , component : DisplayCupboardsPageComponent}, 
  {path: 'AmiPage' , component : AmiPageComponent}, 
  {path: 'ModeratorPage' , component : ModeratorPageComponent}, 
  { path: 'socket-events', loadChildren: () => import('./pages/socket-events/socket-events.module').then(m => m.SocketEventsModule) },
  { path: 'tasks', loadChildren: () => import('./pages/tasks/tasks.module').then(m => m.TasksModule) },
  
  { path: '**', redirectTo: 'home', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
