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
 
package nl.uu.cs.treewidth.output;

import java.io.StringWriter;
import java.util.HashMap;

import nl.uu.cs.treewidth.graph.Edge;
import nl.uu.cs.treewidth.graph.Graph;
import nl.uu.cs.treewidth.graph.NeighborHashSetGraph;
import nl.uu.cs.treewidth.graph.NeighborHashSetEdge;
import nl.uu.cs.treewidth.graph.NeighborHashSetVertex;
import nl.uu.cs.treewidth.graph.TDBag;
import nl.uu.cs.treewidth.graph.Vertex;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NTDBag;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NEdge;

public class DotWriter {
	
	public static <T> String format( Graph<T> g ) {
		StringWriter out = new StringWriter();
		out.write( "graph G {\n\n" );
		
		HashMap<Vertex<T>,String> vertexToName = new HashMap<Vertex<T>,String>();
		int vertexNum = 1;
		for( Vertex<T> v : g.vertices ) {
			String name = "v"+vertexNum++;
			vertexToName.put( v, name );
			out.write( "\t" + name + " [label=\"" + v.data + "\"]\n" );
		}
		
		out.write( "\n" );
		
		for( Edge<T> e : g.getEdges() ) {
			String nameA = vertexToName.get(e.a);
			String nameB = vertexToName.get(e.b);
			out.write( "\t" + nameA + " -- " + nameB + "\n" );
		}
		
		out.write( "\n" ); 
		out.write( "}" );
		return out.toString();
	}
	
	public static <T> String format( NeighborHashSetGraph<T> g ) {
		StringWriter out = new StringWriter();
		out.write( "graph G {\n\n" );
		
		HashMap<NeighborHashSetVertex<T>,String> vertexToName = new HashMap<NeighborHashSetVertex<T>,String>();
		int vertexNum = 1;
		for( NeighborHashSetVertex<T> v : g.vertices ) {
			String name = "v"+vertexNum++;
			vertexToName.put( v, name );
			String label = "" + v.data;
			if( label.equals("") )
				label = name;
			
			
			out.write( "\t" + name + " [label=\"" + label + "\"]\n" );
		}
		
		out.write( "\n" );
		
		for( NeighborHashSetEdge<T> e : g.getEdges() ) {
			String nameA = vertexToName.get(e.a);
			String nameB = vertexToName.get(e.b);
			out.write( "\t" + nameA + " -- " + nameB + "\n" );
		}
		
		out.write( "\n" ); 
		out.write( "}" );
		return out.toString();
	}
	
	public static <D> String format( NGraph<D> g ) {
		StringWriter out = new StringWriter();
		out.write( "graph G {\n\n" );
		
		HashMap<NVertex<D>,String> vertexToName = new HashMap<NVertex<D>,String>();
		int vertexNum = 1;
		for( NVertex<D> v : g ) {
			String name = "v"+vertexNum++;
			vertexToName.put( v, name );
			String label = "" + v.data;
			if( label.equals("") )
				label = name;
			
			
			out.write( "\t" + name + " [label=\"" + label + "\"]\n" );
		}
		
		out.write( "\n" );
		
		for( NEdge<D> e : g.edges() ) {
			String nameA = vertexToName.get(e.a);
			String nameB = vertexToName.get(e.b);
			out.write( "\t" + nameA + " -- " + nameB + "\n" );
		}
		
		out.write( "\n" ); 
		out.write( "}" );
		return out.toString();
	}
	
	public static <D> String formatTD( NGraph<NTDBag<D>> g ) {
		
		StringWriter out = new StringWriter();
		
		out.write( "graph G {\n\n" );
		HashMap<NVertex<NTDBag<D>>,String> bagToName = new HashMap<NVertex<NTDBag<D>>,String>();
		int bagNum = 1;
		for( NVertex<NTDBag<D>> v : g ) {
			String bagName = "bag"+bagNum++;
			bagToName.put( v, bagName );
			out.write( "\t" + bagName + " [label=\"" + v.data.format() + "\"]\n" );
		}
		
		out.write( "\n" );
		
		for( NEdge<NTDBag<D>> e : g.edges() ) {
			String nameA = bagToName.get(e.a);
			String nameB = bagToName.get(e.b);
			out.write( "\t" + nameA + " -- " + nameB + "\n" );
		}
		
		out.write( "\n" ); 
		out.write( "}" );
		
		return out.toString();
		
	}

	public static String formatTD( Graph<TDBag<InputData>> g ) {
		
		StringWriter out = new StringWriter();
		
		out.write( "graph G {\n\n" );
		HashMap<Vertex<TDBag<InputData>>,String> bagToName = new HashMap<Vertex<TDBag<InputData>>,String>();
		int bagNum = 1;
		for( Vertex<TDBag<InputData>> v : g.vertices ) {
			String bagName = "bag"+bagNum++;
			bagToName.put( v, bagName );
			out.write( "\t" + bagName + " [label=\"" + v.data.format() + "\"]\n" );
		}
		
		out.write( "\n" );
		
		for( Edge<TDBag<InputData>> e : g.getEdges() ) {
			String nameA = bagToName.get(e.a);
			String nameB = bagToName.get(e.b);
			out.write( "\t" + nameA + " -- " + nameB + "\n" );
		}
		
		out.write( "\n" ); 
		out.write( "}" );
		
		return out.toString();
		
	}

}
