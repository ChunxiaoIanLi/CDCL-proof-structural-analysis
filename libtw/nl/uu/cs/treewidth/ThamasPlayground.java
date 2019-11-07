/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth;

import java.util.HashSet;

import nl.uu.cs.treewidth.algorithm.CliqueFinder;
import nl.uu.cs.treewidth.input.CliqueGraphGenerator;
import nl.uu.cs.treewidth.input.InputException;
import nl.uu.cs.treewidth.input.RandomGraphGenerator;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

public class ThamasPlayground {

	public static void main( String[] args ) {
		
		NGraph<InputData> g = null;
		try {
			g = new RandomGraphGenerator( 10000, 0.8 ).get();
		} catch (InputException e) {}
		
		CliqueFinder<InputData> f = new CliqueFinder<InputData>();
		
		HashSet<NVertex<InputData>> c = f.maxClique( g );
		
		//g.printGraph( true, false );
		
		for( NVertex<InputData> i : c ) {
			System.out.println( i.data.name );
		}
		
	}
	
}
