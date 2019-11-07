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

import nl.uu.cs.treewidth.algorithm.*;
import nl.uu.cs.treewidth.input.*;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.timing.JavaNanoTime;
import nl.uu.cs.treewidth.timing.Stopwatch;

/**
 * 
 * Little demo program to test the framework.<br />
 * Nothing permanent here; feel free to use it to hack together
 * your own tests for the latest changes.
 * 
 * @author tw team
 *
 */
public class Main {
		
	/**
	 * @param args
	 */
	public static void main(String[] args) {

		System.out.println( "LibTW V1.0\r\n" );
		
		System.out.println( "This library is free software; you can redistribute it and/or ");
		System.out.println( "modify it under the terms of the GNU Lesser General Public");
		System.out.println( "License as published by the Free Software Foundation\r\n" );
		
		NGraph<InputData> g;
		
		
		/* Graph Input
		 *
		 * Read a graph into standard representation
		 * Here you can specify the graph to load.
		 * This graph should be in the /graphs/ library.
		 */
		String graph = "queen5_5.dgf"; 
		GraphInput in = new DgfReader( "graphs/"+graph );
		
		
		try {
			g = in.get(); //Read the graph
		} catch (InputException e) {
			System.out.println( "There was an error opening this file." );
			e.printStackTrace();
			return;
		}
		
		
		/*
		 * Graph Generators. 
		 *
		 * Just uncomment a generator to use it!
		 * (Also uncomment the try & catch under the list)
		 */		
		//GridGraphGenerator gen = new GridGraphGenerator(5,5);
		//NQueenGraphGenerator gen = new NQueenGraphGenerator(3);
		//NKnightGraphGenerator gen = new NKnightGraphGenerator(4);
		//StarGraphGenerator gen = new StarGraphGenerator(10);
		//CliqueGraphGenerator gen = new CliqueGraphGenerator(5);
		//RandomGraphGenerator gen = new RandomGraphGenerator(40,0.45);		
		/*	
		try {
			g = gen.get(); //Generate the graph.
		} catch (InputException e) {
			e.printStackTrace();
		}
		*/
		
		
		//Output some information about the graph
		System.out.println( "  Graph               : "+graph);
		System.out.println( "# Vertices in graph   : "+g.getNumberOfVertices() );
		System.out.println( "# Edges in graph      : "+g.getNumberOfEdges() );	
		System.out.println("");
		
		
		/*
		 * Draw the loaded graph.
		 */
		//Output.toWindow = true; //specify the output source
		//Output.toFile = false;
		//Output.present(g,""); //output the graph
		
		
		/*
		 * We will use a StopWatch to time the algorithms.
		 */
		Stopwatch stopwatch = new Stopwatch(new JavaNanoTime());
		
		
		/* Use a permutation algorithm to compute an upperbound
		 *
		 * Implemented Permutation Algorithms:
		 * -LexBFS
		 * -AllStartLexBFS
		 * -MaximumCardinalitySearch
		 * -AllStartMaximumCardinalitySearch
		 * -MaximumCardinalitySearchMinimal
		 * -AllStartMaximumCardinalitySearchMinimal
		 *
		 *These algorithms return permutations, which must be transformed into a tree decomposition.
		 */
		Permutation<InputData> p = new LexBFS<InputData>(); //The upperbound algorithm
		PermutationToTreeDecomposition<InputData> pttd = new PermutationToTreeDecomposition<InputData>(p);
		stopwatch.reset();
		stopwatch.start();
		pttd.setInput(g);
		pttd.run();
		stopwatch.stop();
		System.out.println("Permutation algorithm : "+p.getName());
		System.out.println("Upperbound            : "+pttd.getUpperBound());
		System.out.println("Time needed           : "+stopwatch.getTime()+" ms");
		System.out.println("");
		
		
		/* Use an upperbound algorihtm.
		 *
		 * Implemented Upperbound Algorithms:
		 * -GreedyDegree
		 * -GreedyFillIn
		 */
		UpperBound<InputData> ub = new GreedyDegree<InputData>();
		stopwatch.reset();
		stopwatch.start();
		ub.setInput(g);
		ub.run();
		stopwatch.stop();
		System.out.println("Upperbound algorithm  : "+ub.getName());
		System.out.println("Upperbound            : "+ub.getUpperBound());
		System.out.println("Time needed           : "+stopwatch.getTime()+" ms");
		System.out.println("");
		
		
		
		/* Use a lowerbound algorihtm.
		 *
		 * Implemented Lowerbound Algorithms:
		 * -MinDegree
		 * -MinorMinWidth
		 * -AllStartMinorMinWidth
		 * -Ramachandramurthi
		 * -MaximumMinimumDegree
		 * -AllStartMaximumMinimumDegree
		 * -MaximumMinimumDegreePlusMinD
		 * -MaximumMinimumDegreePlusMaxD
		 * -MaximumMinimumDegreePlusLeastC
		 * -AllStartMaximumMinimumDegreePlusLeastC
		 */		
		LowerBound<InputData> lb = new MinDegree<InputData>();
		stopwatch.reset();
		stopwatch.start();
		lb.setInput(g);
		lb.run();
		stopwatch.stop();
		System.out.println("Lowerbound algorithm  : "+lb.getName());
		System.out.println("Lowerbound            : "+lb.getLowerBound());
		System.out.println("Time needed           : "+stopwatch.getTime()+" ms");
		System.out.println("");

		
		/*
		 *Run the QuickBB Algorithm
		 */
		QuickBB<InputData> qbb = new QuickBB<InputData>();
		stopwatch.reset();			
		stopwatch.start();
		qbb.setInput(g);
		qbb.run();
		stopwatch.stop();
		System.out.println("Exact algorithm : "+qbb.getName());
		System.out.println("Treewidth       : "+qbb.getUpperBound());
		System.out.println("Time needed     : "+stopwatch.getTime()+" ms");
		System.out.println("");
		
		
		/*
		 *Run the TreeWithDP Algorithm
		 */
		TreewidthDP<InputData> twdp = new TreewidthDP<InputData>( ub.getUpperBound() );
		stopwatch.reset();			
		stopwatch.start();
		twdp.setInput(g);
		twdp.run();
		stopwatch.stop();
		System.out.println("Exact algorithm : "+twdp.getName());
		System.out.println("Treewidth       : "+twdp.getTreewidth());
		System.out.println("Time needed     : "+stopwatch.getTime()+" ms");
		System.out.println("");
		
		System.out.println( "Done." );		
	}
	
}
