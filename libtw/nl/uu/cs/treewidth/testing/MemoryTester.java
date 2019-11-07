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
 
package nl.uu.cs.treewidth.testing;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import nl.uu.cs.treewidth.algorithm.Algorithm;
import nl.uu.cs.treewidth.algorithm.GreedyFillIn;
import nl.uu.cs.treewidth.algorithm.TreewidthDP;
import nl.uu.cs.treewidth.algorithm.UpperBound;
import nl.uu.cs.treewidth.input.DgfReader;
import nl.uu.cs.treewidth.input.GraphInput;
import nl.uu.cs.treewidth.input.InputException;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;

public class MemoryTester {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		if (args.length == 0){
			int startMem = 64;
			// test stuff
			if (!runProgram(startMem)){
				System.err.println("StartMem not big enough!");
				System.exit(1);
			}
			System.out.println("Yeay!");
			int difference = startMem/2;
			int newStartMem = startMem-difference;
			int minStartMem = startMem;
			boolean done = false;
			while (difference > 1  || !done){
				if (difference == 1) done = true;
				difference = (int) Math.ceil((double)difference/(double)2.0);
				if (runProgram(newStartMem)){
					minStartMem = newStartMem;
					newStartMem -= difference;
				} else {
					newStartMem += difference;
				}
			}
			//System.out.println("Difference: "+ difference);
			System.out.println("MinStartMem: " + minStartMem);
			
		} else {
			
			String graph = "graphs/queen7_7.dgf";
			NGraph<InputData> g = null;
			GraphInput in = new DgfReader( graph );
			
			try {
				g = in.get();
			} catch (InputException e) {
				// This is just a demo program; just die.
				System.out.println( "Error opening file; dumping guts." );
				e.printStackTrace();
				return;
			}
			UpperBound<InputData> ubalg = new GreedyFillIn<InputData>();
			ubalg.setInput(g);
			ubalg.run();
			Algorithm<InputData> alg = new TreewidthDP<InputData>(ubalg.getUpperBound());
			
			alg.setInput(g);
			alg.run();
			//System.out.println("Successfully ran "+alg.getName());
		}
		
	}
	
	private static boolean runProgram(int startMem){
		System.out.println("Running with startMem: "+startMem);
		boolean success = false;
		try {
			Process p = null;
			p = Runtime.getRuntime().exec("java -Xmx"+startMem+"M nl.uu.cs.treewidth.testing.MemoryTester test");
			p.waitFor();
			if (p.exitValue() == 0){
				success = true;
			} else {
				success = false;
			}
			InputStreamReader inR = new InputStreamReader( p.getInputStream() );
			BufferedReader buf = new BufferedReader( inR );
			String line;
			while ( ( line = buf.readLine() ) != null ) {
				System.out.println( line );
			} 
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		return success;
		
	}

}
